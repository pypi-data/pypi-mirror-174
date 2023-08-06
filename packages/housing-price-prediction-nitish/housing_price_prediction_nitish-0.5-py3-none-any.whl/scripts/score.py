# python score.py --test_data_independent_path="D:\\mle\\assignment_4\\mle-training\\housing_test_prepared.csv" --test_data_dependent_path="D:\\mle\\assignment_4\\mle-training\\housing_test_labels.csv" --test_prediction_path="D:\\mle\\assignment_4\\mle-training\\test_predicted_data\\" --model_path="D:\\mle\\assignment_4\\mle-training\\" --loging_level="debug"
#  -log_file_path="D:\mle\assignment_4\mle-training\logs"
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from scipy.stats import randint
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error
import argparse
import joblib
from logger import setup_custom_logger
import mlflow
import mlflow.sklearn
from load_constants import Constants
import os


def score_model(
    test_data_independent_path,
    test_data_dependent_path,
    model_path,
    test_prediction_path,
    log_level="debug",
    file_name=None,
):

    logger = setup_custom_logger(__name__, log_level=log_level, file_name=file_name)
    logger.debug("Calling from score file")

    def create_folder(folder_abs_path):
        folder_abs_path = os.path.join(folder_abs_path)
        isExist = os.path.exists(folder_abs_path)
        if not isExist:
            os.makedirs(folder_abs_path, exist_ok=True)
            logger.debug(folder_abs_path + " folder created")
        return folder_abs_path

    test_prediction_path = create_folder(test_prediction_path)

    X_test_prepared = pd.read_csv(test_data_independent_path)
    y_test = pd.read_csv(test_data_dependent_path)
    final_model = joblib.load(model_path + "final_model.pkl")

    final_predictions = final_model.predict(X_test_prepared)
    final_mse = mean_squared_error(y_test, final_predictions)
    final_rmse = np.sqrt(final_mse)

    X_test_prepared_cp = X_test_prepared.copy(deep=True)
    X_test_prepared_cp["predictions"] = final_predictions[:, 1]
    X_test_prepared_cp.to_csv(test_prediction_path + "/scoring.csv")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--test_data_independent_path",
        type=str,
        help="data prep  files folder",
        default=Constants.test_features_path,
    )
    parser.add_argument(
        "--test_data_dependent_path",
        type=str,
        help="data prep  files folder",
        default=Constants.test_labels_path,
    )
    parser.add_argument(
        "--model_path", type=str, help="model  folder", default=Constants.model_path
    )
    parser.add_argument(
        "--test_prediction_path",
        type=str,
        help="scoring folder path",
        default=Constants.test_prediction_path,
    )
    parser.add_argument(
        "--loging_level", type=str, help="loging level", default=Constants.log_level
    )
    parser.add_argument(
        "-log_file_path", type=str, help="loging level", default=Constants.file_name
    )
    args = parser.parse_args()

    score_model(
        args.test_data_independent_path,
        args.test_data_dependent_path,
        args.model_path,
        args.test_prediction_path,
        log_level=args.loging_level,
        file_name=args.log_file_path,
    )
