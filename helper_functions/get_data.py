import pandas as pd
import yfinance as yf
import datetime as dt


def get_sp500_tickers():
    tickers = pd.read_html(
        'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].str.replace('.', '-').unique().tolist()
    return tickers

def get_small_cap_plus_tickers():
    df = pd.read_csv('small_cap_plus.csv')
    return df['Symbol'].to_list()

def get_stocks_data(list_name='SP500', start_date=dt.datetime(1950, 1, 1), end_date=dt.datetime.now(), interval='1D'):
    if list_name == 'SP500':
        tickers_lst = get_sp500_tickers()
    else: 
        tickers_lst = get_stocks_data()

    df = yf.download(tickers=tickers_lst,
        start=start_date,
        end=end_date)
    return df
