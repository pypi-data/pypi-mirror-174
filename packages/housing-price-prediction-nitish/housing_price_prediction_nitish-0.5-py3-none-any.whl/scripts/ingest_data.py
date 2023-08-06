# python ingest_data.py --input_folder="https://raw.githubusercontent.com/ageron/handson-ml2/master/"  --output_folder="src\\data\\output\\model_input_files\\"--loging_level="debug"

# -log_file_path=".\\log_file"
import os
import tarfile
import numpy as np
import argparse
import pandas as pd
from six.moves import urllib
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.impute import SimpleImputer
import mlflow
import mlflow.sklearn
from logger import setup_custom_logger
from load_constants import Constants


def data_ingest(input_folder, output_folder, log_level="debug", file_name=None):

    logger = setup_custom_logger(__name__, log_level=log_level, file_name=file_name)
    logger.debug("Calling from ingest data file")
    output_folder = os.path.join(output_folder)
    isExist = os.path.exists(output_folder)
    if not isExist:
        os.makedirs(output_folder, exist_ok=True)
        logger.debug("output folder created")

    # DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml2/master/"
    DOWNLOAD_ROOT = input_folder

    HOUSING_PATH = os.path.join("datasets", "housing")
    HOUSING_URL = DOWNLOAD_ROOT + "datasets/housing/housing.tgz"

    def fetch_housing_data(housing_url=HOUSING_URL, housing_path=HOUSING_PATH):
        os.makedirs(housing_path, exist_ok=True)
        tgz_path = os.path.join(housing_path, "housing.tgz")
        urllib.request.urlretrieve(housing_url, tgz_path)
        housing_tgz = tarfile.open(tgz_path)
        housing_tgz.extractall(path=housing_path)
        housing_tgz.close()

    def load_housing_data(housing_path=HOUSING_PATH):
        csv_path = os.path.join(housing_path, "housing.csv")
        return pd.read_csv(csv_path)

    fetch_housing_data()
    housing = load_housing_data()
    print(housing.head())

    train_set, test_set = train_test_split(housing, test_size=0.2, random_state=42)

    housing["income_cat"] = pd.cut(
        housing["median_income"],
        bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
        labels=[1, 2, 3, 4, 5],
    )

    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    for train_index, test_index in split.split(housing, housing["income_cat"]):
        strat_train_set = housing.loc[train_index]
        strat_test_set = housing.loc[test_index]

    def income_cat_proportions(data):
        return data["income_cat"].value_counts() / len(data)

    train_set, test_set = train_test_split(housing, test_size=0.2, random_state=42)

    compare_props = pd.DataFrame(
        {
            "Overall": income_cat_proportions(housing),
            "Stratified": income_cat_proportions(strat_test_set),
            "Random": income_cat_proportions(test_set),
        }
    ).sort_index()
    compare_props["Rand. %error"] = (
        100 * compare_props["Random"] / compare_props["Overall"] - 100
    )
    compare_props["Strat. %error"] = (
        100 * compare_props["Stratified"] / compare_props["Overall"] - 100
    )

    for set_ in (strat_train_set, strat_test_set):
        set_.drop("income_cat", axis=1, inplace=True)

    housing = strat_train_set.copy()
    housing.plot(kind="scatter", x="longitude", y="latitude")
    housing.plot(kind="scatter", x="longitude", y="latitude", alpha=0.1)

    corr_matrix = housing.corr()
    corr_matrix["median_house_value"].sort_values(ascending=False)
    housing["rooms_per_household"] = housing["total_rooms"] / housing["households"]
    housing["bedrooms_per_room"] = housing["total_bedrooms"] / housing["total_rooms"]
    housing["population_per_household"] = housing["population"] / housing["households"]

    housing = strat_train_set.drop(
        "median_house_value", axis=1
    )  # drop labels for training set
    housing_labels = strat_train_set["median_house_value"].copy()

    imputer = SimpleImputer(strategy="median")

    housing_num = housing.drop("ocean_proximity", axis=1)

    imputer.fit(housing_num)
    X = imputer.transform(housing_num)

    housing_tr = pd.DataFrame(X, columns=housing_num.columns, index=housing.index)
    housing_tr["rooms_per_household"] = (
        housing_tr["total_rooms"] / housing_tr["households"]
    )
    housing_tr["bedrooms_per_room"] = (
        housing_tr["total_bedrooms"] / housing_tr["total_rooms"]
    )
    housing_tr["population_per_household"] = (
        housing_tr["population"] / housing_tr["households"]
    )

    housing_cat = housing[["ocean_proximity"]]
    housing_prepared = housing_tr.join(pd.get_dummies(housing_cat, drop_first=True))

    X_test = strat_test_set.drop("median_house_value", axis=1)
    y_test = strat_test_set["median_house_value"].copy()

    X_test_num = X_test.drop("ocean_proximity", axis=1)
    X_test_prepared = imputer.transform(X_test_num)
    X_test_prepared = pd.DataFrame(
        X_test_prepared, columns=X_test_num.columns, index=X_test.index
    )
    X_test_prepared["rooms_per_household"] = (
        X_test_prepared["total_rooms"] / X_test_prepared["households"]
    )
    X_test_prepared["bedrooms_per_room"] = (
        X_test_prepared["total_bedrooms"] / X_test_prepared["total_rooms"]
    )
    X_test_prepared["population_per_household"] = (
        X_test_prepared["population"] / X_test_prepared["households"]
    )

    X_test_cat = X_test[["ocean_proximity"]]
    X_test_prepared = X_test_prepared.join(pd.get_dummies(X_test_cat, drop_first=True))

    housing_prepared.to_csv(output_folder + "\housing_prepared.csv")
    housing_labels.to_csv(output_folder + "\housing_labels.csv")

    X_test_prepared.to_csv(output_folder + "\housing_test_prepared.csv")
    y_test.to_csv(output_folder + "\housing_test_labels.csv")
    print(output_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_folder",
        type=str,
        help="input files folder",
        default=Constants.input_folder,
    )
    parser.add_argument(
        "--output_folder",
        type=str,
        help="output files folder",
        default=Constants.output_folder,
    )
    parser.add_argument(
        "--loging_level", type=str, help="loging level", default=Constants.log_level
    )
    parser.add_argument(
        "-log_file_path", type=str, help="loging level", default=Constants.file_name
    )
    args = parser.parse_args()

    data_ingest(
        input_folder=args.input_folder,
        output_folder=args.output_folder,
        log_level=args.loging_level,
        file_name=args.log_file_path,
    )
