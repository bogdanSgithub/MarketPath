import pandas as pd


def get_sp500_tickers():

    tickers = pd.read_html(
        'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    return tickers

def get_small_cap_plus_tickers():
    df = pd.read_csv('small_cap_plus.csv')
    df = df.sort_values(by='Symbol')
    df['Symbol'].to_csv('small_cap_plus.csv', index=False)

