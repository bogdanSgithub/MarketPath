import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import plotly.express as px

firms = [
    "Morgan Stanley",
    "Citigroup",
    "Deutsche Bank",
    "Barclays",
    "JP Morgan",
    "UBS",
    "Jefferies",
    "Raymond James",
    "Bank of America",
    "Wells Fargo",
    "KeyBanc",
    "BMO Capital",
    "Goldman Sachs",
    "Oppenheimer",
    "Nomura",
    "Baird",
    "SunTrust Robinson Humphrey",
    "Canaccord Genuity",
    "PiperJaffray",
    "B of A Securities",
    "Wedbush",
    "Cowen & Co.",
    "Macquarie",
    "Needham",
    'Bernstein',
    'Stifel',
    'JMP Securities'
]

df = pd.read_excel('analysts.xlsx', index_col=False)

columns = [ 'Ticker',
    'Rating', 'Rating Firm', 'Date', 'Date after 1 Week', 'Date after 4 weeks', 'Date after 12 weeks',
    '% change 1 week stock price', '% change 4 week stock price',
    '% change 12 week stock price', '% change 1 week SPY price', '% change 4 week SPY price',
    '% change 12 week SPY price'
]
df = df[columns]

important_ratings = df[df['Rating Firm'].isin(firms)]
print(important_ratings.Rating.unique())

ratings = ['Neutral', 'Overweight', 'Buy', 'Hold', 'Underweight', 'Equal-Weight',
 'Market Perform', 'Sell', 'Underperform', 'Outperform', 'Perform',
 'Sector Weight', 'Equal-weight', 'Outperformer', 'Market Outperform',
 'Strong Buy', 'Cautious', 'Reduce', 'Conviction Buy', 'Top Pick',
 'Above Average', 'Hold Neutral', 'Market Underperform', 'Market Weight',
 'Sector Perform', 'Underperformer', 'In-line', 'In-Line']

positive_ratings = [
    'Buy',
    'Overweight',
    'Strong Buy',
    'Conviction Buy',
    'Top Pick',
    'Outperform',
    'Outperformer',
    'Market Outperform',
    'Above Average'
]

df = pd.read_excel('analysts.xlsx', index_col=False)

jp_ratings = df[df['Rating Firm'] == 'JP Morgan'].dropna()
# create a dictionary of replacements
replacements = {
    'Outperform': 'Overweight',
    'Neutral': 'Hold',
    'Underweight': 'Underweight',
    'Overweight': 'Overweight',
    'Buy': 'Buy',
    'Sell': 'Sell',
    'Hold': 'Hold'
    }

# replace values using the .map() method
jp_ratings['Rating'] = jp_ratings['Rating'].map(replacements)

import plotly.express as px
def plot_histogram(df, column, name='Plot'):
    fig = px.histogram(df, x=column, title=name)
    fig.show()