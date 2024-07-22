import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

TRAINING_DATASET_PATH = "data/training.csv"
MODEL_PATH = "model.pkl"
OUTPERFORMANCE = 10

def status_calc(stock, sp500):
    """A simple function to classify whether a stock outperformed the S&P500
    :param stock: stock price
    :param sp500: S&P500 price
    :return: true/false
    """
    return stock - sp500 >= OUTPERFORMANCE

def build_data_set():
    """
    Reads the keystats.csv file and prepares it for scikit-learn
    :return: X_train and y_train numpy arrays
    """
    training_data = pd.read_csv(TRAINING_DATASET_PATH, index_col="Date")

    training_data.dropna(axis=0, how="any", inplace=True)
    features = training_data.columns[7:]

    X_train = training_data[features].values
    # Generate the labels: '1' if a stock beats the S&P500 by more than 10%, else '0'.
    y_train = list(
        status_calc(
            training_data["stock_p_change"],
            training_data["SP500_p_change"]
        )
    )
    return X_train, y_train

def train_model():
    X_train, y_train = build_data_set()
    model = RandomForestClassifier(n_estimators=100, random_state=0)
    model.fit(X_train, y_train)
    joblib.dump(model, MODEL_PATH)
    return model

# Load or train model
def get_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return train_model()
