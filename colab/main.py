import streamlit as st
import pandas as pd
import datetime as dt
import yfinance as yf
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# Page Config
st.set_page_config(
    page_title='MarketPath',
    page_icon='🏛️',
    layout='centered'
)

# Navigation
selected = option_menu(
    menu_title=None,
    options=['Product', 'Roadmap', 'Something else'],
    icons = ['bar-chart-line', 'map', 'map'],
    menu_icon='cast',
    default_index=0,
    orientation='horizontal'
)

st.title('Market Path')

df_train = pd.read_csv('training.csv', index_col='Date')
df_val = pd.read_csv('validation.csv', index_col='Date')
df_pred = pd.read_csv('prediction.csv', index_col='Date')

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
    symbol = st.selectbox(label='Select a Stock Symbol', label_visibility='collapsed', placeholder='AAPL', options=tickers)
    
    # Get OHLC and display
    df_stock_price = get_historical_price(symbol)

    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df_stock_price.index, open=df_stock_price['Open'], high=df_stock_price['High'], low=df_stock_price['Low'], close=df_stock_price['Close']) )

    fig.update_layout(height=800)
    st.plotly_chart(fig)

    #with st.expander("See more"):
    #    st.write(f'''
    #        The chart above shows the historical price of {symbol} from {start_date} to {end_date}
    #    ''')

    df_stock_data = df_pred[df_pred['Ticker'] == symbol]
    # Number of columns per section
    cols_per_section = 10

    # Display DataFrame in chunks
    for i in range(df_stock_data.shape, cols_per_section):
        chunk = df_stock_data.iloc[:, i:i + cols_per_section]
        st.write(chunk)

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