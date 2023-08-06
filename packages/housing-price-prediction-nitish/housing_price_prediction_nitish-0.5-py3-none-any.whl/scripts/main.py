import mlflow
import mlflow.sklearn
from logger import setup_custom_logger
from ingest_data import data_ingest
from train import train_model
from score import score_model
from load_constants import Constants


if __name__ == "__main__":

    data_ingest(
        input_folder=Constants.input_folder,
        output_folder=Constants.output_folder,
        log_level=Constants.log_level,
        file_name=Constants.file_name,
    )
    train_model(
        Constants.train_features_path,
        Constants.train_labels_path,
        Constants.model_path,
        Constants.train_prediction_path,
        log_level=Constants.log_level,
        file_name=Constants.file_name,
    )

    score_model(
        Constants.test_features_path,
        Constants.test_labels_path,
        Constants.model_path,
        Constants.test_prediction_path,
        log_level=Constants.log_level,
        file_name=Constants.file_name,
    )
