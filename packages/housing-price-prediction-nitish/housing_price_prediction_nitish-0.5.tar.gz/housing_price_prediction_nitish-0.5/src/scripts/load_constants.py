from cmath import log
from datetime import timedelta, datetime
import yaml
from io import open
import os


def get_config_data(file_path):
    print("file path", file_path)
    """
    This Function reads Yml config file required for constants
    """
    with open(file_path, "r", encoding="utf8") as fp:
        cfg = yaml.safe_load(fp)
    return cfg


# print(os.getcwd() + "\src\conf\config.yml")
config_data = get_config_data(os.getcwd() + "\src\conf\config.yml")


class Constants:
    """
    This class contains all the constants variables
    """

    # Databases
    input_folder = config_data["input_folder"]
    output_folder = config_data["output_folder"]
    train_features_path = config_data["train_features_path"]
    train_labels_path = config_data["train_labels_path"]
    model_path = config_data["model_path"]
    train_prediction_path = config_data["train_prediction_path"]
    test_features_path = config_data["test_features_path"]
    test_labels_path = config_data["test_labels_path"]
    test_prediction_path = config_data["test_prediction_path"]
    log_level = config_data["log_level"]
    file_name = None  # ".\\log_file"
