import streamlit as st
import pandas as pd
import datetime as dt
import yfinance as yf
import joblib
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# Page Config
st.set_page_config(
    page_title='MarketPath',
    page_icon='🏛️',
    layout='centered'
)
st.title('Market Path')

# Navigation
selected = option_menu(
    menu_title=None,
    options=['Product', 'Roadmap', 'Something else'],
    icons = ['bar-chart-line', 'map', 'map'],
    menu_icon='cast',
    default_index=0,
    orientation='horizontal'
)

df_train = pd.read_csv('data/training.csv', index_col='Date')
df_val = pd.read_csv('data/validation.csv', index_col='Date')
df_pred = pd.read_csv('data/prediction.csv', index_col='Date')
model = joblib.load('model.pkl')

tickers = df_pred['Ticker'].to_list()

start_date = dt.datetime.strptime("2023-01-01", "%Y-%m-%d")
end_date = dt.datetime.now().strftime("%Y-%m-%d")

def get_historical_price(stock: str, start: str = "2023-01-01", end: str = dt.datetime.now().strftime("%Y-%m-%d"), interval: str = '1d'):
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")
    df = yf.download(stock, start=start_date, end=end_date, interval=interval)
    return df

def product():
    # Get symbol
    st.write('#### Select a Stock Symbol')
    symbol = st.selectbox(label='Select a Stock Symbol', label_visibility='collapsed', placeholder='AAPL', options=tickers, index=None)
    
    if symbol is not None:
        # Get OHLC data
        df_stock_price = get_historical_price(symbol)

        # Display OHLC data
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=df_stock_price.index, open=df_stock_price['Open'], high=df_stock_price['High'], low=df_stock_price['Low'], close=df_stock_price['Close']) )
        fig.update_layout(height=800)
        st.plotly_chart(fig)

        # Get Financial data
        df_stock_data = df_pred[df_pred['Ticker'] == symbol]

        valuation_metrics = [
        "Market Cap",
        "Enterprise Value",
        "Trailing P/E",
        "Forward P/E",
        "PEG Ratio",
        "Price/Sales",
        "Price/Book",
        "Enterprise Value/Revenue",
        "Enterprise Value/EBITDA"
        ]

        profitability_metrics = [
            "Profit Margin",
            "Operating Margin",
            "Return on Assets",
            "Return on Equity"
        ]

        financial_metrics = [
            "Revenue",
            "Revenue Per Share",
            "EBITDA",
            "Net Income Avl to Common",
            "Diluted EPS",
            "Total Cash",
            "Total Cash Per Share",
            "Total Debt",
            "Total Debt/Equity",
            "Current Ratio",
            "Book Value Per Share"
        ]

        market_metrics = [
            "Beta",
            "50-Day Moving Average",
            "200-Day Moving Average",
            "Avg Vol (3 month)",
            "Shares Outstanding"
        ]

        df_transposed = df_stock_data.transpose()

        # Split the DataFrame into four parts based on your lists
        valuation_df = df_transposed.loc[valuation_metrics]
        profitability_df = df_transposed.loc[profitability_metrics]
        financial_df = df_transposed.loc[financial_metrics]
        market_df = df_transposed.loc[market_metrics]

        # Streamlit layout with two columns
        col1, col2 = st.columns(2)
        WIDTH = 600
        HEIGHT = 422

        # Display the tables in Streamlit
        with col1:
            st.subheader("Valuation Metrics")
            st.dataframe(valuation_df, width=WIDTH, height=HEIGHT)

            st.subheader("Market Metrics")
            st.dataframe(market_df, width=WIDTH)

        with col2:
            st.subheader("Financial Metrics")
            st.dataframe(financial_df, width=WIDTH, height=HEIGHT)

            st.subheader("Profitability Metrics")
            st.dataframe(profitability_df, width=WIDTH)
        
        prediction = model.predict(df_stock_data.iloc[:, 1:])
        if prediction:
            st.write("#### Model's Prediction: BUY")
        else:
            st.write("#### Model's Prediction: SELL")
    


def roadmap():
    # Datasets
    st.write('## Datasets')
    st.write('#### Training/Testing Dataset (2003-2013)')
    st.write(df_train)
    st.write('#### Validation Dataset (2017-2018)')
    st.write(df_val)

if selected == 'Product':
    product()
elif selected == 'Roadmap':
    roadmap()
else:
    pass

# run: streamlit run main.py --theme.base="dark" -- theme.primaryColor="#228b22"