""" python train.py --train_data_independent_path="src\\data\\output\\model_input_files\\housing_prepared.csv" --train_data_dependent_path="src\\data\\output\\model_input_files\\housing_labels.csv" --prediction_path="src\\data\\output\\model_output_files\\predicted_data\\" --model_path="src\\data\\output\\model_output_files\\model_pkl\\"  --loging_level="debug"
 -log_file_path=".\\log_file"  """
import os
import pdb
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.tree import DecisionTreeRegressor
from scipy.stats import randint
import argparse
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV

# from sklearn.externals import joblib
import joblib
from logger import setup_custom_logger
import mlflow
import mlflow.sklearn
from load_constants import Constants


def train_model(
    train_data_independent_path,
    train_data_dependent_path,
    model_path,
    prediction_path,
    log_level="debug",
    file_name=None,
):

    logger = setup_custom_logger(__name__, log_level=log_level, file_name=file_name)
    logger.debug("Calling from train  file")

    def create_folder(folder_abs_path):
        folder_abs_path = os.path.join(folder_abs_path)
        isExist = os.path.exists(folder_abs_path)
        if not isExist:
            os.makedirs(folder_abs_path, exist_ok=True)
            logger.debug(folder_abs_path + " folder created")
        return folder_abs_path

    prediction_path = create_folder(prediction_path)
    model_path = create_folder(model_path)
    housing_prepared = pd.read_csv(train_data_independent_path)
    housing_labels = pd.read_csv(train_data_dependent_path)

    """linear model"""
    lin_reg = LinearRegression()
    lin_reg.fit(housing_prepared, housing_labels)

    lr_housing_predictions = lin_reg.predict(housing_prepared)
    housing_prepared_lr_copy = housing_prepared.copy(deep=True)
    #
    housing_prepared_lr_copy["predictions"] = lr_housing_predictions[:, 1]
    # pdb.set_trace()
    housing_prepared_lr_copy.to_csv(prediction_path + "\\lr_prediction.csv")
    lin_mse = mean_squared_error(housing_labels, lr_housing_predictions)
    lin_rmse = np.sqrt(lin_mse)

    mlflow.log_artifact(prediction_path + "\\lr_prediction.csv")

    """decison tree model"""
    tree_reg = DecisionTreeRegressor(random_state=42)
    tree_reg.fit(housing_prepared, housing_labels)

    tr_housing_predictions = tree_reg.predict(housing_prepared)
    housing_prepared_tr_copy = housing_prepared.copy(deep=True)
    housing_prepared_tr_copy["predictions"] = tr_housing_predictions[:, 1]
    housing_prepared_tr_copy.to_csv(prediction_path + "tr_prediction.csv")
    tree_mse = mean_squared_error(housing_labels, tr_housing_predictions)
    tree_rmse = np.sqrt(tree_mse)

    """random forest model"""
    param_grid = [
        # try 12 (3×4) combinations of hyperparameters
        {"n_estimators": [3, 10, 30], "max_features": [2, 4, 6, 8]},
        # then try 6 (2×3) combinations with bootstrap set as False
        {
            "bootstrap": [False],
            "n_estimators": [3, 10],
            "max_features": [2, 3, 4],
        },
    ]

    forest_reg = RandomForestRegressor(random_state=42)
    # train across 5 folds, that's a total of (12+6)*5=90 rounds of training
    grid_search = GridSearchCV(
        forest_reg,
        param_grid,
        cv=5,
        scoring="neg_mean_squared_error",
        return_train_score=True,
    )
    grid_search.fit(housing_prepared, housing_labels)

    grid_search.best_params_
    cvres = grid_search.cv_results_
    for mean_score, params in zip(cvres["mean_test_score"], cvres["params"]):
        print(np.sqrt(-mean_score), params)

    feature_importances = grid_search.best_estimator_.feature_importances_
    sorted(zip(feature_importances, housing_prepared.columns), reverse=True)

    rf_final_model = grid_search.best_estimator_
    rf_housing_predictions = rf_final_model.predict(housing_prepared)
    housing_prepared_rf_copy = housing_prepared.copy(deep=True)
    housing_prepared_rf_copy["predictions"] = rf_housing_predictions[:, 1]
    housing_prepared_rf_copy.to_csv(prediction_path + "rf_prediction.csv")
    rf_rmse = mean_squared_error(housing_labels, rf_housing_predictions)
    rf_rmse = np.sqrt(rf_rmse)

    if lin_rmse < tree_rmse and lin_rmse < rf_rmse:
        final_model = lin_rmse
        final_prediction = housing_prepared_lr_copy
    elif tree_rmse < lin_rmse and tree_rmse < rf_rmse:
        final_model = tree_reg
        final_prediction = housing_prepared_tr_copy
    elif rf_rmse < lin_rmse and rf_rmse < tree_rmse:
        final_model = rf_final_model
        final_prediction = housing_prepared_rf_copy

    joblib.dump(final_model, model_path + "final_model.pkl")
    final_prediction.to_csv(prediction_path + "prediction.csv")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--train_data_independent_path",
        type=str,
        help="data prep  files folder",
        default=Constants.train_features_path,
    )
    parser.add_argument(
        "--train_data_dependent_path",
        type=str,
        help="data prep  files folder",
        default=Constants.train_labels_path,
    )
    parser.add_argument(
        "--prediction_path",
        type=str,
        help="prediction files folder",
        default=Constants.train_prediction_path,
    )
    parser.add_argument(
        "--model_path", type=str, help="model  folder", default=Constants.model_path
    )
    parser.add_argument(
        "--loging_level",
        type=str,
        help="loging level",
        default=Constants.log_level,
    )
    parser.add_argument(
        "-log_file_path", type=str, help="loging level", default=Constants.file_name
    )
    args = parser.parse_args()

    train_model(
        args.train_data_independent_path,
        args.train_data_dependent_path,
        args.model_path,
        args.prediction_path,
        log_level=args.loging_level,
        file_name=args.log_file_path,
    )
