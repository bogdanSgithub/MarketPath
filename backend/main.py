from fastapi import FastAPI
import json
import uvicorn
import pandas as pd
import yfinance as yf
import datetime as dt
from train_model import get_model
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PREDICTIONS_DATASET_PATH = "data/final_2024-07-23.csv"

@app.get("/")
async def root():
    return {"message": "Hello World"}

# get list of sp500 tickers
@app.get("/sp500_tickers")
async def get_sp500_tickers():
    tickers = pd.read_csv(PREDICTIONS_DATASET_PATH)['Ticker']
    return tickers.to_list()

@app.get('/data/{stock}')
async def get_data(stock: str):
    data_df = pd.read_csv(PREDICTIONS_DATASET_PATH)
    data = data_df[data_df['Ticker'] == stock].reset_index().to_dict(orient='records')
    historical_df = await get_historical_data(stock)
    return (data, historical_df)

@app.get("/historical_data/{stock}")
async def get_historical_data(stock: str, start: str = "2023-01-01", end: str = dt.datetime.now().strftime("%Y-%m-%d"), interval: str = '1d'):
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")
    df = yf.download(stock, start=start_date, end=end_date, interval=interval)
    return df.reset_index().to_dict(orient='records')

'''
@app.get("/predict/")
async def predict(file_path: str = TESTING_DATASET_PATH):
    df = pd.read_csv(file_path, index_col="Date")
    features = df.columns[7:]
    X_test = df[features].values
    model = get_model()
    predictions = model.predict(X_test)

    df['Date'] = df.index
    predictions_series = pd.Series(predictions, name='Predictions', index=df.index)

    # Concatenate predictions with the original DataFrame
    final = pd.concat([df[['Date', 'Ticker', 'stock_p_change', 'SP500_p_change']], predictions_series], axis=1).to_json(orient="records")
    return json.loads(final)
'''
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)