import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import joblib
import os


TRAINING_DATASET_PATH = "data/training.csv"
MODEL_PATH = "model.pkl"
OUTPERFORMANCE = 10

def prepare_data(df):
    df = df.drop('Gross Profit', axis=1)
    df.dropna(axis=0, how="any", inplace=True)

    features = df.columns[5:]
    print(features)
    #display(features.shape)
    x = df[features]

    scaler = StandardScaler()
    # Fit and transform the data
    x = pd.DataFrame(scaler.fit_transform(x), columns=x.columns)

    y = df['stock_p_change'] - df['SP500_p_change'] > OUTPERFORMANCE
    z = np.array(df[["stock_p_change", "SP500_p_change"]])
    return x, y, z

def analyze_model(y_test, y_pred, z_test):
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    cm = confusion_matrix(y_test, y_pred)
    cm_display = ConfusionMatrixDisplay(confusion_matrix = cm, display_labels = [0, 1])
    cm_display.plot()
    plt.show()

    stock_returns = 1 + z_test[y_pred, 0] / 100
    market_returns = 1 + z_test[y_pred, 1] / 100

    num_positive_predictions = sum(y_pred)

    # Calculate the average growth for each stock we predicted 'buy'
    # and the corresponding index growth
    avg_predicted_stock_growth = sum(stock_returns) / num_positive_predictions
    index_growth = sum(market_returns) / num_positive_predictions
    percentage_stock_returns = 100 * (avg_predicted_stock_growth - 1)
    percentage_market_returns = 100 * (index_growth - 1)
    total_outperformance = percentage_stock_returns - percentage_market_returns

    print("\n Stock prediction performance report \n", "=" * 40)
    print(f"Total Trades:", num_positive_predictions)
    print(f"Average return for stock predictions: {percentage_stock_returns: .1f} %")
    print(f"Average market return in the same period: {percentage_market_returns: .1f}% ")
    print(f"Compared to the index, our strategy earns {total_outperformance: .1f} percentage points more")

def train_model():
    data_df = pd.read_csv(TRAINING_DATASET_PATH, index_col="Date")
    X, y, z = prepare_data(data_df)
    X_train, X_test, y_train, y_test, z_train, z_test = train_test_split(
        X, y, z, test_size=0.2)

    model = RandomForestClassifier(n_estimators=100, random_state=0)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    joblib.dump(model, MODEL_PATH)

    analyze_model(y_test, y_pred, z_test)
    return model

# Load or train model
def get_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return train_model()
