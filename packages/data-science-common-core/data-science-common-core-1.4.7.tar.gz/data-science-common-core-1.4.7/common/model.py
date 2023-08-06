"""Machine learning model."""
import logging
import os
import pickle
from multiprocessing import cpu_count

import numpy as np
import pandas as pd
import pgzip
from catboost import CatBoostClassifier, CatBoostRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.multioutput import MultiOutputRegressor
from src.logic import export_predictions
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.layers import Dense, Dropout, Input, Normalization
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adamax

from .custom_hgb import CustomHistGradientBoostingClassifier
from .custom_multi import CustomMultiOutputClassifier
from .io import (
    fetch_from_bucket,
    get_data_bucket,
    get_storage_client,
    insert_logs,
    insert_metrics,
    insert_to_sheet,
    logger,
    upload_to_bucket,
)
from .logic import (
    calculate_mean_absolute_error,
    calculate_mean_average_precision,
    kappa_analysis,
)
from .plot import plot_model_results
from .query import q_delete_run


def nn_model_setup(params, num_input, num_output, df_norm) -> Sequential:
    """Design the nn model architecture.

    Args:
        params (dict)       : NN parameters
        num_input (int)     : no. of input variables
        num_output (int)    : no. of output variables
        df_norm (dataframe) : chunk of data for normalization
    Returns:
        model (keras.models.Sequential): untrained NN model
    """
    # Model design
    model = Sequential()
    l_in = Input(num_input)
    model.add(l_in)
    l_n = Normalization(axis=1)
    l_n.adapt(df_norm)
    model.add(l_n)

    nn_params = params["model_params_nn"]

    # Stack Dense layers
    for idx_layer in range(nn_params["no_layers"]):
        # Set number of neurons for the current layer
        no_neurons = int(nn_params["basic_neurons"] / (2**idx_layer))

        # Add Dense layer and dropout
        model.add(
            Dense(
                no_neurons,
                activation=nn_params["activation"],
                kernel_initializer=nn_params["kernel_init"],
            )
        )
        model.add(Dropout(nn_params["dropout"]))

    # Last predictive layer
    if nn_params["last_activation"] != "":
        model.add(Dense(num_output, activation=nn_params["last_activation"]))
    else:
        model.add(Dense(num_output))

    # Compile model
    model.compile(
        loss=nn_params["loss"],
        optimizer=Adamax(learning_rate=nn_params["learning_rate"]),
        metrics=nn_params["metrics"],
    )

    print(model.summary())

    return model


def ml_setup(params, num_input, num_output, df):
    """Model-agnostic setup, initialize the model object."""
    model_type = params["model_type"]
    if model_type == "nn":
        model = nn_model_setup(
            params,
            num_input,
            num_output,
            df,
        )
    # Allocate here with wanted scikit-learn classifiers
    elif model_type == "hgb":
        model_params = params["model_params_hgb"].copy()
        model_params.pop("model_file")

        if params["prediction_type"] == "classification":
            model = hgb_classification_model_setup(params)
        else:
            model = hgb_regressor_model_setup(params)
    elif model_type == "cat":
        if params["ft_encoding"] is not None:
            logging.warning(
                "Catboost performs best with no/minimal feature preprocessing."
                " Ohe/pca to categorical features should be avoided."
            )
        if params["prediction_type"] == "classification":
            model = cat_classification_model_setup(params)
        else:
            model = cat_regressor_model_setup(params)
    else:
        raise ValueError

    return model


def ml_load(params, data):
    """Model-agnostic loading."""
    msg = "Download model file"
    logger.info(msg)
    insert_logs(params, msg)

    model_type = params["model_type"]
    if model_type == "nn":
        model_path = fetch_from_bucket(params, "model")["model"]
        model = ml_setup(
            params, data["data_num_input"], data["data_num_output"], data["df_test"]
        )
        model.load_weights(model_path)
    else:
        model = fetch_from_bucket(params, "model")["model"]

    return model


def sk_train(params, model, data):
    """Fit multi-output scikit-learn classifier and store the model file."""
    if params["prediction_type"] == "classification":
        params["smote_params"]["categorical_features"] = [0]
        params["smote_params"]["random_state"] = params["random_state"]

        multi_model = CustomMultiOutputClassifier(model, n_jobs=1)
        multi_model.fit(
            data["df_train"],
            data["label_train"],
            eval_set=(data["df_val"], data["label_val"]),
        )
    elif params["prediction_type"] == "regression":
        multi_model = MultiOutputRegressor(model)
        multi_model.fit(data["df_train"], data["label_train"])

    if not params["dry_run"]:
        with pgzip.open(
            params[f"model_params_{params['model_type']}"]["path_model_file"],
            "wb",
            blocksize=2**22,
            compresslevel=4,
            thread=cpu_count(),
        ) as f:
            pickle.dump(multi_model, f)

    return multi_model


def nn_train(params, model, data) -> Sequential:
    """Train of the neural network model.

    Returns:
        model (keras.models.Sequential): trained NN model object
    """
    # # Generators
    # training_generator = DataGenerator(params, data, mode="train")
    # validation_generator = DataGenerator(params, data, mode="val")

    nn_params = params["model_params_nn"]

    # Setup callbacks
    es = EarlyStopping(
        monitor=nn_params["metric_monitor"],
        mode=nn_params["metric_mode"],
        min_delta=nn_params["early_stopping_min_delta"],
        verbose=nn_params["verbose"],
        patience=nn_params["patience"],
    )
    mc = ModelCheckpoint(
        filepath=nn_params["path_model_file"],
        monitor=nn_params["metric_monitor"],
        mode=nn_params["metric_mode"],
        verbose=nn_params["verbose"],
        save_best_only=True,
    )

    # Model training
    model.fit(
        x=data["df_train"],
        y=data["label_train"],
        validation_data=(data["df_val"], data["label_val"]),
        epochs=nn_params["max_epochs"],
        batch_size=nn_params["batch_size"],
        callbacks=[es, mc],
        workers=8,
        use_multiprocessing=True,
        max_queue_size=10,
        verbose=nn_params["verbose"],
    )

    return model


def ml_train(params, model, data):
    """Model-agnostic training."""
    model_type = params["model_type"]
    if model_type == "nn":
        model = nn_train(params, model, data)
    else:
        model = sk_train(params, model, data)
    return model


def ml_predict(params, model, df):
    """Model-agnostic predict function."""
    model_type = params["model_type"]
    if model_type == "nn" or params["prediction_type"] == "regression":
        # Compute prediction on validation data
        df_pred = model.predict(df)
    else:
        # Compute prediction on validation data for each model
        df_pred = np.array([i[:, 1] for i in model.predict_proba(df)]).T

    return df_pred


def ml_upload(params):
    """Model-agnostic upload to bucket."""
    model_params = params[f'model_params_{params["model_type"]}']

    # Upload FeatureTransformer file - if existing
    if os.path.exists(params["path_ft_file"]):
        upload_to_bucket(
            params,
            params["path_ft_file"],
            "",
            bucket_folder="ft",
        )

    # Upload model file
    upload_to_bucket(params, model_params["path_model_file"], "", bucket_folder="model")

    return


def model_evaluation(params, data):
    """Measure the performances of a model with/out teu normalization.

    Args:
    data (dict): data dictionary in order to evaluate the model.
    """
    results = {}
    if params["prediction_type"] == "classification":
        results = calculate_mean_average_precision(params, data)
        results.update(kappa_analysis(params, data))

    elif params["prediction_type"] == "regression":
        results = calculate_mean_absolute_error(params, data)

    else:
        raise ValueError(
            "Prediction_type should either be 'classification' or 'regression'"
        )

    return results


def ml_performance(params, model, data):
    """Model-agnostic performance evaluation."""
    # Train mode
    if params["train_mode"]:
        # Compute prediction on validation data
        df_pred = ml_predict(params, model, data["df_val"])
        data["pred_val"] = pd.DataFrame(df_pred, columns=params["data_output_fields"])
        data["pred_val"].index = data["id_val"][params["id_field"]]

        results = model_evaluation(params, data)

        if params["plot"]:
            plot_model_results(params, data, results)

        # Upload the data if not in dry run
        if not params["dry_run"]:
            # upload metrics to the dwh
            insert_metrics(params, results)
            ml_upload(params)

        msg = "Training is complete."
        logger.info(msg)
        insert_logs(params, msg)

    # Test mode
    else:
        msg = "Predict test results and compute performances"
        logger.info(msg)
        insert_logs(params, msg)

        data["pred_test"] = ml_predict(params, model, data["df_test"])

        # Compute prediction on test data and store result metrics
        export_predictions(params, data)
        msg = "Prediction is complete."
        logger.info(msg)
        insert_logs(params, msg)

    return model


def hgb_regressor_model_setup(params):
    """Create HistGradientBoosting Regressor."""
    # Select hgb parameters
    model_params = params["model_params_hgb"]

    # Set up HistGradientBoosting model
    model = HistGradientBoostingRegressor(
        max_iter=model_params["max_iter"],
        max_leaf_nodes=model_params["max_leaf_nodes"],
        l2_regularization=model_params["l2_regularization"],
        loss=model_params["loss"],
        learning_rate=model_params["learning_rate"],
        scoring=model_params["scoring"],
        early_stopping=model_params["early_stopping"],
        tol=model_params["tol"],
        n_iter_no_change=model_params["n_iter_no_change"],
        random_state=model_params["random_state"],
        verbose=model_params["verbose"],
    )

    return model


def hgb_classification_model_setup(params):
    """Create HistGradientBoosting Regressor."""
    # Select hgb parameters
    model_params = params["model_params_hgb"]

    # Set up HistGradientBoosting model
    model = CustomHistGradientBoostingClassifier(
        max_iter=model_params["max_iter"],
        max_leaf_nodes=model_params["max_leaf_nodes"],
        l2_regularization=model_params["l2_regularization"],
        loss=model_params["loss"],
        learning_rate=model_params["learning_rate"],
        scoring=model_params["scoring"],
        early_stopping=model_params["early_stopping"],
        tol=model_params["tol"],
        n_iter_no_change=model_params["n_iter_no_change"],
        random_state=model_params["random_state"],
        verbose=model_params["verbose"],
    )

    return model


def cat_classification_model_setup(params):
    """Create CatBoostClassifier."""
    model_params = params["model_params_cat"]["model_kwargs"]
    model = CatBoostClassifier(
        cat_features=params["processed_cat_features"], **model_params
    )

    return model


def cat_regressor_model_setup(params):
    """Create CatBoostRegressor."""
    model_params = params["model_params_cat"]["model_kwargs"]
    model = CatBoostRegressor(
        cat_features=params["processed_cat_features"], **model_params
    )

    return model


def ml_model(params, data):
    """Model-agnostic main function."""
    if params["model_type"] not in ["nn", "hgb", "cat"]:
        logger.log("Invalid model type, options: `nn`, `hgb`, and `cat`")

    else:
        if params["train_mode"]:
            model = ml_setup(
                params,
                data["data_num_input"],
                data["data_num_output"],
                data["df_train"][::10],
            )
            model = ml_train(params, model, data)
        else:
            model = ml_load(params, data)

        model = ml_performance(params, model, data)
    return model


def prune_model(params, model_id=None):
    """Prune model files and info from GBQ and GCS."""
    if not model_id and "model_id" in params:
        model_id = params["model_id"]

    # Fetch CGS client and list blobs
    client = get_storage_client(params)
    bucket = get_data_bucket(params, client)
    blobs = bucket.list_blobs()

    # Delete objects from GCS - if present
    for blob in blobs:
        if model_id in blob.name:
            blob.delete()
            logger.info(f"{blob.name} successfully deleted from Google Cloud Storage!")

    # Delete record from GBQ
    q_delete_run(params, model_id)

    return


def compute_performance_table(params, data_segment, mode):
    """Compute and export percentile performance tables."""
    # Compute percentiles
    data_segment["count_range"] = range(data_segment.shape[0])
    data_segment["percentile"] = (
        np.ceil(100 * ((1 + data_segment["count_range"]) / data_segment.shape[0]))
    ).astype(int)

    # Compute percentile aggregations
    agg_label = {"conversion_label": ["count", "sum", "mean"]}
    agg_score = {"conversion_score": ["min", "max", "mean"]}
    agg_label.update(agg_score)
    aggregation = agg_score if mode == "test" else agg_label
    percentile = data_segment.groupby("percentile").agg(aggregation).reset_index()

    # Reindex columns
    percentile.columns = ["_".join(col) for col in percentile.columns]

    if mode != "test":
        # Compute cumulative statistics
        for metric in ["count", "sum"]:
            percentile[f"cum_conv_label_{metric}"] = percentile[
                f"conversion_label_{metric}"
            ].cumsum()

        percentile["Cum Mean Score"] = (
            percentile.conversion_score_mean * percentile.conversion_label_count
        ).cumsum() / percentile.conversion_label_count.cumsum()
        percentile["Cum Target %"] = (
            percentile.cum_conv_label_sum / percentile.cum_conv_label_count
        )

        # Compute lift and recall
        percentile["Cum Lift"] = (
            percentile["Cum Target %"] / percentile["Cum Target %"].iloc[-1]
        )
        percentile["Recall %"] = (
            percentile.cum_conv_label_sum / percentile.cum_conv_label_sum.iloc[-1]
        )

        percentile = percentile.rename(
            {
                "conversion_label_count": "# obs",
                "conversion_label_sum": "# target",
                "conversion_label_mean": "Target %",
                "cum_conv_label_count": "Cum obs",
                "cum_conv_label_sum": "Cum target",
            },
            axis=1,
        )

    percentile = percentile.rename(
        {
            "percentile_": "percentile",
            "conversion_score_min": "Min score",
            "conversion_score_max": "Max score",
            "conversion_score_mean": "Mean score",
        },
        axis=1,
    )

    insert_to_sheet(
        params, percentile, mode=f"res_{mode}", replace=True, include_index=False
    )

    return


def performance_lift(params, data, model):
    """Compute lift."""
    # Compute scores and actuals for trainval data
    for segment in ["train", "val", "test"]:
        # Compute prediction on data segment
        data[f"pred_{segment}"] = pd.DataFrame(
            ml_predict(params, model, data[f"df_{segment}"]),
            columns=params["data_output_fields"],
        )

        try:
            if segment == "test":
                # Add segment index
                data[f"pred_{segment}"].index = data[f"df_{segment}"].index

                data[f"check_{segment}"] = (
                    data[f"pred_{segment}"]
                    .rename({"conversion": "conversion_score"}, axis=1)
                    .sort_values("conversion_score", ascending=False)
                )

            # Add label
            else:
                # Add segment index
                data[f"pred_{segment}"].index = data[f"id_{segment}"][
                    params["id_field"]
                ]

                data[f"check_{segment}"] = (
                    data[f"label_{segment}"]
                    .join(data[f"pred_{segment}"], lsuffix="_label", rsuffix="_score")
                    .sort_values("conversion_score", ascending=False)
                )

            compute_performance_table(params, data[f"check_{segment}"], mode=segment)

        except KeyError:
            logger.warning(f"{segment} data are not available to export")

    # Join data and sort by prediction score, descending
    data["check_total"] = pd.concat(
        [data["check_train"], data["check_val"]]
    ).sort_values("conversion_score", ascending=False)

    compute_performance_table(params, data["check_total"], mode="total")

    return
