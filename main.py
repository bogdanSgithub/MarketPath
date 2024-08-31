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
    page_icon='ðŸ�›ï¸�',
    layout='centered'
)
st.title('Market Path')

# Navigation
selected = option_menu(
    menu_title=None,
    options=['Forecast', 'Watchlist', 'Roadmap'],
    icons = ['bar-chart-line', 'card-checklist', 'map'],
    menu_icon='cast',
    default_index=0,
    orientation='horizontal'
)

# dataframes and model
df_train = pd.read_csv('data/training.csv', index_col='Date')
df_val = pd.read_csv('data/validation.csv', index_col='Date')
df_pred = pd.read_csv('data/prediction.csv', index_col='Date')
model = joblib.load('model.pkl')

tickers = df_pred['Ticker'].to_list()

start_date = dt.datetime.strptime("2023-01-01", "%Y-%m-%d")
end_date = dt.datetime.now()
pred_start_date = dt.datetime.strptime(df_pred.index[0], "%Y-%m-%d")
pred_end_date = pred_start_date.replace(year=pred_start_date.year + 1)

def get_historical_price(stock: str, start: str = "2023-01-01", end: str = dt.datetime.now().strftime("%Y-%m-%d"), interval: str = '1d'):
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")
    df = yf.download(stock, start=start_date, end=end_date, interval=interval, progress=False)
    return df

def Forecast():
    # Get symbol
    st.write('#### Select a Stock Symbol')
    symbol = st.selectbox(label='Select a Stock Symbol', label_visibility='collapsed', placeholder='AAPL', options=tickers, index=None)
    
    st.write("")
    st.write("")
    if symbol is not None:
        # Get OHLC data
        df_stock_price = get_historical_price(symbol)

        # Get Financial data
        df_stock_data = df_pred[df_pred['Ticker'] == symbol]
        company_name = df_stock_data['Company Name'].values[0]

        # Display OHLC data
        st.write(f"### {company_name} Stock Price Evolution {start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}")
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=df_stock_price.index, open=df_stock_price['Open'], high=df_stock_price['High'], low=df_stock_price['Low'], close=df_stock_price['Close']) )
        fig.update_layout(height=800)
        st.plotly_chart(fig)

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
        
        prediction = model.predict(df_stock_data.iloc[:, 2:])
        
        if prediction:
            st.markdown("# Model's Prediction: :green[BUY]")
            st.write(f'##### The model predicts {symbol} to **OUTPERFORM** the market by 10% from {pred_start_date.strftime("%Y-%m-%d")} until {pred_end_date.strftime("%Y-%m-%d")}')
        else:
            st.markdown("# Model's Prediction: :red[SELL]")
            st.write(f'##### The model predicts {symbol} to **NOT OUTPERFORM** the market by 10% from {pred_start_date.strftime("%Y-%m-%d")} until {pred_end_date.strftime("%Y-%m-%d")}')
    
def Watchlist():
    X = df_pred.iloc[:, 2:]
    predictions = model.predict(X)

    preds = pd.Series(predictions, name='Predictions')
    merged = pd.concat([df_pred.reset_index(drop=True), preds.reset_index(drop=True)], axis=1)

    df_winners = merged[merged['Predictions'] == True].set_index('Ticker')
    st.write("### Model's Watchlist: Stocks Predicted to Beat the Market")
    st.write(f'##### From {pred_start_date.strftime("%Y-%m-%d")} Until {pred_end_date.strftime("%Y-%m-%d")}')
    st.dataframe(df_winners, width=800, height=878)

def Roadmap():
    # Project Overview
    st.subheader("Project Overview ðŸš€")
    st.write("""
    Navigating the stock market can be both exciting and daunting. With its potential for significant financial gain comes the risk, especially for those who are new to investing. **MarketPath** aims to simplify this journey, making the stock market more accessible and less intimidating for beginners. By providing intuitive insights and predictions, we help users make informed investment decisions with confidence.
    """)

    # Problem Identification
    st.subheader("Problem Identification ðŸ”�")
    st.write("**Objective:**")
    st.write("""
    The goal is to develop a model that predicts which S&P 500 stocks will outperform the market over the next 12 months. Leveraging advanced machine learning techniques, the model provides actionable insights to guide investment strategies.
    """)

    st.write("**Why It Matters:**")
    st.write("""
    Discovering stocks poised to beat the market can significantly enhance investment decisions, leading to potential financial growth and a more secure financial future.
    """)

    # Target Audience
    st.subheader("Target Audience ðŸŽ¯")
    st.write("""
    The tool is designed for both novice and seasoned investors. It provides valuable data-driven predictions on which S&P 500 stocks are likely to outperform the market, helping users refine their investment strategies.
    """)

    # Scope and Constraints
    st.subheader("Scope and Constraints ðŸ“Š")
    st.write("""
    The AI tool will analyze financial data from S&P 500 stocks to forecast which ones may exceed the market's performance by 10% over the next year.
    """)
    st.write('### DISCLAMER')
    st.write('##### Past performance does not guarantee future results. Use MarketPath AI to enhance your investment strategy, but be mindful of the risks involved in stock market investing.')

    # Datasets
    st.subheader("Datasets ðŸ“�")
    st.write(f"""
    Three datasets are used:
    - **Training/Testing:** 2003-2013 from [Python Programming](https://pythonprogramming.net/data-acquisition-machine-learning/)""")
    st.write(df_train)
    st.write(f'- **Testing:** 2017-2018 from the same source')
    st.write(df_val)
    st.write('- **Prediction:** 2024 from [Yahoo Finance](https://ca.finance.yahoo.com/quote/NVDA/)')
    st.write(df_pred)

    # Data Collection and Exploration
    st.subheader("Data Collection and Exploration ðŸ”Ž")
    st.write("""
    - Searched the web and scraped data to gather financial information.
    - Iteratively refined features to enhance model performance.
    - Removed features with high percentages of missing values (NaN).
    - Conducted exploratory data analysis to understand data patterns and distributions.
    """)

    # Model Selection and Training ðŸ”§
    st.subheader("Model Selection and Training ðŸ”§")
    st.write("""
    **Models Tested:** Logistic Regression, K-Nearest Neighbors (KNN), Decision Tree Classifier, Random Forest Classifier.

    **Training Process:** 
    - Handled NaN values, converted features to integers, and performed feature engineering to optimize the model. 
    - Split the initial dataset (2003-2013) into 80% training and 20% testing, while using subsequent datasets (2017-2018 and 2024) for further testing and predictions.

    **Evaluation Metrics:** 
    - Used confusion matrix and compared the average percent change of predicted stocks to the market over 12 months.

    **Success Criteria:** 
    - Stocks predicted to beat the market should indeed outperform it.

    **Results:** 
    - The Random Forest Classifier proved to be the most accurate model.
    """)

    # Ethical Considerations
    st.subheader("Ethical Considerations ðŸ¤�")
    st.write("""
    - **Transparency:** Past performance does not guarantee future results. Use MarketPath AI to enhance your investment strategy, but be mindful of the risks involved in stock market investing.
    - **Data Privacy:** Data used was open source and free to use.
    """)

    # Future Steps
    st.subheader("Future Steps ðŸš€")
    st.write("""
    - **Enhance Feature Engineering:** Refine feature selection and transformation to boost model accuracy.
    - **Update Data:** Collect and integrate data from more recent years to keep predictions relevant and accurate.
    """)


if selected == 'Forecast':
    Forecast()
elif selected == 'Watchlist':
    Watchlist()
else:
    Roadmap()

footer="""<style>
a:link , a:visited{
color: #FAFAFA;
background-color: transparent;
}

a:hover, a:active {
    color: #228b22;
    background-color: transparent;
    text-decoration: none;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: #0E1117;
color: #FAFAFA;
text-align: center;
}
</style>
<div class="footer">
<p>Developed by <a style='display: block; text-align: center;' href="https://github.com/bogdanSgithub" target="_blank">Bogdan Andrei Feher</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)

# run: streamlit run main.py --theme.base="dark" --theme.primaryColor="#228b22"