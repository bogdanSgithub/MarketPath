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

company_names = [
    "3M Company", "AbbVie Inc.", "Accenture plc", "Adobe Inc.",
    "Advanced Micro Devices, Inc.", "The AES Corporation", 
    "Agilent Technologies, Inc.", "Air Products and Chemicals, Inc.",
    "Airbnb, Inc.", "Akamai Technologies, Inc.", "Align Technology, Inc.",
    "Allegion plc", "Alliant Energy Corporation", "Alphabet Inc. (Class A)",
    "Alphabet Inc. (Class C)", "Amazon.com, Inc.", "Amcor plc", 
    "Ameren Corporation", "American Electric Power Company, Inc.", 
    "American Tower Corporation", "American Water Works Company, Inc.", 
    "AMETEK, Inc.", "Amgen Inc.", "Amphenol Corporation", 
    "Analog Devices, Inc.", "ANSYS, Inc.", "Apple Inc.", 
    "Applied Materials, Inc.", "Aptiv PLC", "Arista Networks, Inc.", 
    "AT&T Inc.", "Atmos Energy Corporation", "Autodesk, Inc.", 
    "Automatic Data Processing, Inc.", "AvalonBay Communities, Inc.", 
    "Avery Dennison Corporation", "Baker Hughes Company", "Ball Corporation", 
    "Best Buy Co., Inc.", "Biogen Inc.", "BorgWarner Inc.", 
    "Boston Scientific Corporation", "Bristol-Myers Squibb Company", 
    "Broadcom Inc.", "Broadridge Financial Solutions, Inc.", 
    "Brown-Forman Corporation", "Bunge Limited", "Boston Properties, Inc.", 
    "Caesars Entertainment, Inc.", "Campbell Soup Company", "CarMax, Inc.", 
    "Carrier Global Corporation", "Caterpillar Inc.", "CBRE Group, Inc.", 
    "Celanese Corporation", "CoreSite Realty Corporation", 
    "Centene Corporation", "CenterPoint Energy, Inc.", "C.H. Robinson Worldwide, Inc.",
    "Charles River Laboratories International, Inc.", "Charter Communications, Inc.", 
    "Chevron Corporation", "Chipotle Mexican Grill, Inc.", 
    "Church & Dwight Co., Inc.", "Cintas Corporation", 
    "Cisco Systems, Inc.", "The Clorox Company", "CME Group Inc.", 
    "CMS Energy Corporation", "The Coca-Cola Company", "Cognizant Technology Solutions Corporation",
    "Colgate-Palmolive Company", "Comcast Corporation", "Conagra Brands, Inc.", 
    "ConocoPhillips", "Consolidated Edison, Inc.", "Constellation Brands, Inc.", 
    "The Cooper Companies, Inc.", "Copart, Inc.", "Corning Incorporated", 
    "Catalent, Inc.", "Corteva, Inc.", "CoStar Group, Inc.", 
    "Costco Wholesale Corporation", "CrowdStrike Holdings, Inc.", 
    "Crown Castle Inc.", "CSX Corporation", "Cummins Inc.", 
    "CVS Health Corporation", "Danaher Corporation", 
    "Darden Restaurants, Inc.", "DaVita Inc.", "DoorDash, Inc.", 
    "Deere & Company", "Delta Air Lines, Inc.", "Devon Energy Corporation", 
    "DexCom, Inc.", "Digital Realty Trust, Inc.", "Dollar General Corporation", 
    "Dollar Tree, Inc.", "Dominion Energy, Inc.", "Dover Corporation", 
    "Dow Inc.", "D.R. Horton, Inc.", "DTE Energy Company", 
    "Duke Energy Corporation", "DuPont de Nemours, Inc.", "Eastman Chemical Company", 
    "Eaton Corporation plc", "Ecolab Inc.", "Edison International", 
    "Edwards Lifesciences Corporation", "Electronic Arts Inc.", 
    "Enphase Energy, Inc.", "Entergy Corporation", "EOG Resources, Inc.", 
    "EQT Corporation", "Equifax Inc.", "Equinix, Inc.", 
    "Equity Residential", "Essex Property Trust, Inc.", 
    "The Estée Lauder Companies Inc.", "Evergy, Inc.", 
    "Exelon Corporation", "Expedia Group, Inc.", "Expeditors International of Washington, Inc.", 
    "Extra Space Storage Inc.", "Exxon Mobil Corporation", 
    "F5, Inc.", "FactSet Research Systems Inc.", 
    "Fastenal Company", "Fidelity National Information Services, Inc.", 
    "First Solar, Inc.", "FirstEnergy Corp.", "Fiserv, Inc.", 
    "Ford Motor Company", "Fortive Corporation", "Fox Corporation", 
    "Fox Corporation", "Franklin Resources, Inc.", 
    "Garmin Ltd.", "General Electric Company", 
    "Gen Digital Inc.", "Generac Holdings Inc.", 
    "General Dynamics Corporation", "General Mills, Inc.", 
    "General Motors Company", "Genuine Parts Company", 
    "Gilead Sciences, Inc.", "Global Payments Inc.", 
    "Halliburton Company", "Hasbro, Inc.", "HCA Healthcare, Inc.", 
    "Henry Schein, Inc.", "The Hershey Company", "Hess Corporation", 
    "Hewlett Packard Enterprise Company", "Hologic, Inc.", 
    "The Home Depot, Inc.", "Honeywell International Inc.", 
    "Hormel Foods Corporation", "Host Hotels & Resorts, Inc.", 
    "Howmet Aerospace Inc.", "Hubbell Incorporated", 
    "Huntington Ingalls Industries, Inc.", "International Business Machines Corporation", 
    "IDEX Corporation", "IDEXX Laboratories, Inc.", 
    "Illinois Tool Works Inc.", "Incyte Corporation", 
    "Ingersoll Rand Inc.", "Insulet Corporation", 
    "Intel Corporation", "Intercontinental Exchange, Inc.", 
    "International Paper Company", "The Interpublic Group of Companies, Inc.", 
    "Intuitive Surgical, Inc.", "Invesco Ltd.", "Invitation Homes Inc.", 
    "IQVIA Holdings Inc.", "Jack Henry & Associates, Inc.", 
    "Jacobs Engineering Group Inc.", "Johnson Controls International plc", 
    "Juniper Networks, Inc.", "Kellogg Company", 
    "Keurig Dr Pepper Inc.", "Keysight Technologies, Inc.", 
    "Kimberly-Clark Corporation", "Kinder Morgan, Inc.", 
    "KLA Corporation", "The Kraft Heinz Company", 
    "The Kroger Co.", "L3Harris Technologies, Inc.", 
    "Laboratory Corporation of America Holdings", 
    "Lam Research Corporation", "Lamb Weston Holdings, Inc.", 
    "Las Vegas Sands Corp.", "Lennar Corporation", 
    "Eli Lilly and Company", "Linde plc", 
    "Live Nation Entertainment, Inc.", "LKQ Corporation", 
    "Lockheed Martin Corporation", "Lululemon Athletica Inc.", 
    "LyondellBasell Industries N.V.", "Marathon Petroleum Corporation", 
    "MarketAxess Holdings Inc.", "Marsh & McLennan Companies, Inc.", 
    "Martin Marietta Materials, Inc.", "Mastercard Incorporated", 
    "McCormick & Company, Incorporated", "Medtronic plc", 
    "Merck & Co., Inc.", "Meta Platforms, Inc.", 
    "MGM Resorts International", "Microchip Technology Incorporated", 
    "Microsoft Corporation", "Molson Coors Beverage Company", 
    "Mondelez International, Inc.", "Monolithic Power Systems, Inc.", 
    "Monster Beverage Corporation", "Moody's Corporation", 
    "The Mosaic Company", "Motorola Solutions, Inc.", 
    "Nasdaq, Inc.", "NetApp, Inc.", "Netflix, Inc.", 
    "Newmont Corporation", "News Corporation", 
    "News Corporation", "NextEra Energy, Inc.", 
    "NiSource Inc.", "Nordson Corporation", 
    "Norfolk Southern Corporation", "Northrop Grumman Corporation", 
    "Norwegian Cruise Line Holdings Ltd.", "NVIDIA Corporation", 
    "NXP Semiconductors N.V.", "Occidental Petroleum Corporation", 
    "Old Dominion Freight Line, Inc.", "Omnicom Group Inc.", 
    "ON Semiconductor Corporation", "ONEOK, Inc.", 
    "Oracle Corporation", "PACCAR Inc", 
    "Packaging Corporation of America", 
    "Palo Alto Networks, Inc.", "Parker-Hannifin Corporation", 
    "Paychex, Inc.", "PayPal Holdings, Inc.", 
    "Pentair plc", "PepsiCo, Inc.", "PG&E Corporation", 
    "Pinnacle West Capital Corporation", 
    "PPG Industries, Inc.", "PPL Corporation", 
    "The Procter & Gamble Company", "Public Service Enterprise Group Incorporated", 
    "PTC Inc.", "Public Storage", "PulteGroup, Inc.", 
    "Quanta Services, Inc.", "QUALCOMM Incorporated", 
    "Quest Diagnostics Incorporated", "Ralph Lauren Corporation", 
    "Raytheon Technologies Corporation", "Realty Income Corporation", 
    "Regency Centers Corporation", "Regeneron Pharmaceuticals, Inc.", 
    "Republic Services, Inc.", "ResMed Inc.", 
    "Revvity, Inc.", "Rockwell Automation, Inc.", 
    "Rollins, Inc.", "Roper Technologies, Inc.", 
    "Ross Stores, Inc.", "Royal Caribbean Group", 
    "S&P Global Inc.", "Salesforce, Inc.", 
    "ServiceNow, Inc.", "The Sherwin-Williams Company", 
    "Simon Property Group, Inc.", "Skyworks Solutions, Inc.", 
    "The J.M. Smucker Company", "Snap-on Incorporated", 
    "The Southern Company", "Southwest Airlines Co.", 
    "Steel Dynamics, Inc.", "STERIS plc", 
    "Stryker Corporation", "Synopsys, Inc.", 
    "Sysco Corporation", "T-Mobile US, Inc.", 
    "T. Rowe Price Group, Inc.", "Tapestry, Inc.", 
    "Targa Resources Corp.", "Target Corporation", 
    "TE Connectivity Ltd.", "Teleflex Incorporated", 
    "Teradyne, Inc.", "Tesla, Inc.", 
    "Texas Instruments Incorporated", "Textron Inc.", 
    "Thermo Fisher Scientific Inc.", "The TJX Companies, Inc.", 
    "Tractor Supply Company", "Trane Technologies plc", 
    "Trimble Inc.", "Tyler Technologies, Inc.", 
    "Uber Technologies, Inc.", "Ulta Beauty, Inc.", 
    "Union Pacific Corporation", "United Airlines Holdings, Inc.", 
    "United Parcel Service, Inc.", "United Rentals, Inc.", 
    "UnitedHealth Group Incorporated", "Verisk Analytics, Inc.", 
    "Verizon Communications Inc.", "Vertex Pharmaceuticals Incorporated", 
    "Viatris Inc.", "Visa Inc.", "Vistra Corp.", 
    "Vulcan Materials Company", "W.W. Grainger, Inc.", 
    "Walgreens Boots Alliance, Inc.", "Walmart Inc.", 
    "The Walt Disney Company", "Waste Management, Inc.", 
    "Waters Corporation", "WEC Energy Group, Inc.", 
    "Welltower Inc.", "West Pharmaceutical Services, Inc.", 
    "Weyerhaeuser Company", "Williams Companies, Inc.", 
    "Willis Towers Watson Public Limited Company", 
    "Xcel Energy Inc.", "Xylem Inc.", "Zebra Technologies Corporation", 
    "Zimmer Biomet Holdings, Inc.", "Zoetis Inc."
]

start_date = dt.datetime.strptime("2023-01-01", "%Y-%m-%d")
end_date = dt.datetime.now()

def get_historical_price(stock: str, start: str = "2023-01-01", end: str = dt.datetime.now().strftime("%Y-%m-%d"), interval: str = '1d'):
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")
    df = yf.download(stock, start=start_date, end=end_date, interval=interval)
    return df

def product():
    # Get symbol
    st.write('#### Select a Stock Symbol')
    symbol = st.selectbox(label='Select a Stock Symbol', label_visibility='collapsed', placeholder='AAPL', options=tickers, index=None)
    
    st.write("")
    st.write("")
    if symbol is not None:
        company_name = company_names[tickers.index(symbol)]
        # Get OHLC data
        df_stock_price = get_historical_price(symbol)

        # Display OHLC data
        st.write(f"### {company_name} Stock Price Evolution {start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}")
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

        date = dt.datetime.strptime(df_stock_data.index[0], "%Y-%m-%d")
        date_1_year_later = date.replace(year=date.year + 1)
        
        if prediction:
            st.markdown("# Model's Prediction: :green[BUY]")
            st.write(f'##### The model predicts {symbol} to **OUTPERFORM** the market by 10% from {date.strftime("%Y-%m-%d")} until {date_1_year_later.strftime("%Y-%m-%d")}')
        else:
            st.markdown("# Model's Prediction: :red[SELL]")
            st.write(f'##### The model predicts {symbol} to **NOT OUTPERFORM** the market by 10% from {date.strftime("%Y-%m-%d")} until {date_1_year_later.strftime("%Y-%m-%d")}')
        
        #st.write('### DISCLAMER')
        #st.write('##### Past performance does not guarantee future results. Use MarketPath AI to enhance your investment strategy, but #be mindful of the risks involved in stock market investing.')
    


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