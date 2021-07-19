"""
    File name: movingAverage.py
    Author: Timothy Clark
    Date created: 6/26/2021
    Date last modified: 6/26/2021
    Python Version: 3.8

    Description: Runs a Simple Moving Average (SMA) algorithim on the stock ticker provided.
    The short term and long terma rolling means can be adjusted to create a Dual Moving
    Average (DMA) model
"""

import alpaca_trade_api as tradeapi
import constants
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None  # default='warn'


api = tradeapi.REST(
    constants.API_KEY,
    constants.API_SECRET_KEY,
    constants.MARKET
)

def maModel(ticker):
    # get daily stock data for the ticker provided
    barset = api.get_barset(ticker, 'day', limit=300).df
    tickerdata = barset[ticker]
    day = np.arange(1, len(tickerdata) + 1)
    tickerdata['day']= day

    # Calculate rolling averages per day
    tickerdata['9-day'] = tickerdata['close'].rolling(1).mean()
    tickerdata['21-day'] = tickerdata['close'].rolling(20).mean()

    # add a signal for buy or sell
    tickerdata['signal'] = np.where(tickerdata['9-day'] > tickerdata['21-day'], 1, 0)
    tickerdata['signal'] = np.where(tickerdata['9-day'] < tickerdata['21-day'], -1, tickerdata['signal'])
    tickerdata.dropna(inplace=True)

    # create a flag for when to create buy or sell transaction
    tickerdata['return'] = np.log(tickerdata['close']).diff()
    tickerdata['system_return'] = tickerdata['signal'] * tickerdata['return']
    tickerdata['transactionFlag'] = tickerdata.signal.diff()

    return tickerdata.loc[tickerdata.index[-1],'transactionFlag']


###################################################
# Functions maPlot and maPerformance              #
# are strictly for testing and research purposes  #
###################################################

def maPlot(gld):
    plt.rcParams['figure.figsize'] = 12, 6
    plt.grid(True, alpha = .3)
    plt.plot(gld.iloc[-208:]['close'], label = 'GLD')
    plt.plot(gld.iloc[-208:]['9-day'], label = '9-day')
    plt.plot(gld.iloc[-208:]['21-day'], label = '21-day')
    plt.plot(gld[-208:].loc[gld.transactionFlag == 2].index, gld[-208:]['9-day'][gld.transactionFlag == 2], '^',
             color = 'g', markersize = 12)
    plt.plot(gld[-208:].loc[gld.transactionFlag == -2].index, gld[-208:]['21-day'][gld.transactionFlag == -2], 'v',
             color = 'r', markersize = 12)
    plt.legend(loc=2)
    plt.show()

def maPerformance(gld):
    plt.plot(np.exp(gld['return']).cumprod(), label='Buy/Hold')
    plt.plot(np.exp(gld['system_return']).cumprod(), label='System')
    plt.legend(loc=2)
    plt.grid(True, alpha=.3)
    plt.show()








