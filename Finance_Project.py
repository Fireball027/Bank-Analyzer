from pandas_datareader import data, wb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import plotly
import cufflinks as cf
sns.set_style('whitegrid')
cf.go_offline()


# Data
start = datetime.datetime(2006, 1, 1)
end = datetime.datetime(2016, 1, 1)

# Bank Of America
BAC = data.DataReader('BAC', 'google', start, end)
# CitiGroup
C = data.DataReader('C', 'google', start, end)
# Goldman Sachs
GS = data.DataReader('GS', 'google', start, end)
# JPMorgan Chase
JPM = data.DataReader('JPM', 'google', start, end)
# Morgan Stanley
MS = data.DataReader('MS', 'google', start, end)
# Wells Fargo
WFC = data.DataReader('WFC', 'google', start, end)

# Create a list of the ticker symbols in alphabetical order
tickers = ['BAC', 'C', 'GS', 'JPM', 'MS', 'WFC']

# Concatenate the bank dataframes together into single data frame
bank_stocks = pd.concat([BAC, C, GS, JPM, MS, WFC], axis=1, keys=tickers)
# bank_stocks.head()

# Set the column name levels
bank_stocks.columns.names = ['Bank Ticker', 'Stock Info']
bank_stocks.head()


# Exploratory Data Analysis (EDA)
# What is the max Close Price for each bank's stock throughout the time period?
bank_stocks.xs(key='Close', axis=1, level='Stock Info').max()

# Create a new empty DataFrame. It should contain the returns for each bank's stock
returns = pd.DataFrame()

# Use a method on the Close column to create a column representing this return value
for tick in tickers:
    returns[tick + ' Return'] = bank_stocks[tick]['Close'].pct_change()
returns.head()

# Create a pairplot of the returns dataframe
sns.pairplot(returns[1:])

# Using this returns DataFrame, figure out on what dates each bank stock had the best and worst single day returns
returns.idxmax()
returns.idxmin()

# Look at standard deviation of the returns. Classify the riskiest stock
returns.std()
returns.ix['2015-01-01':'2015-12-31'].std()  # 2015's

# Create a distplot of the 2015 returns for Morgan Stanley
sns.distplot(returns.ix['2015-01-01':'2015-12-31']['MS Return'],
             color='green', bins=50)

# Create a distplot of the 2008 returns for CitiGroup
sns.distplot(returns.ix['2008-01-01':'2008-12-31']['C Return'],
             color='red', bins=50)


# Visualizations
# Create a line plot showing close price for each bank for the entire index of time
for tick in tickers:
    bank_stocks[tick]['Close'].plot(label=tick, figsize=(12, 4))
plt.legend()

bank_stocks.xs(key='Close', axis=1, level='Stock Info').plot()  # cross-section Method
bank_stocks.xs(key='Close', axis=1, level='Stock Info').iplot()  # plotly Method

# Moving Averages
# Plot the rolling 30-day average against the Close Price for Bank Of America's stock for 2008
BAC['Close'].ix['2008-01-01':'2009-01-01'].rolling(window=30).mean().plot(label='30 Day Mov Avg')
BAC['Close'].ix['2008-01-01':'2009-01-01'].plot(label='BAC Close')
plt.legend()

# Create a heatmap of the correlation between the stocks Close Price
sns.heatmap(bank_stocks.xs(key='Close', axis=1, level='Stock Info').corr(), annot=True)

sns.clustermap(bank_stocks.xs(key='Close', axis=1, level='Stock Info').corr(), annot=True)    # clustermap

# plotly cufflinks
close_corr = bank_stocks.xs(key='Close', axis=1, level='Stock Info').corr()
close_corr.iplot(kind='heatmap', colorscale='rdylbu')


# Technical Analysis Plots
# Create a candle plot of Bank Of America's stock from Jan 1st 2015 to Jan 1st 2016
bac15 = BAC[['Open', 'High', 'Low', 'Close']].ix['2015-01-01':'2016-01-01']
bac15.iplot(kind='candle')

# Create a Simple Moving Averages fo Morgan Stanley for the year 2015
MS['Close'].ix['2015-01-01':'2016-01-01'].ta_plot(study='sma', periods=[13, 21, 55])

# Create a Bollinger Band Plot for Bank Of America for the year 2015
BAC['Close'].ix['2015-01-01':'2016-01-01'].ta_plot(study='boll')
