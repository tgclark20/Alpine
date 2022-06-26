"""
    File name: movingAverage.py
    Author: Timothy Clark
    Date created: 6/26/2021
    Date last modified: 05/29/2022
    Python Version: 3.9

    Description: Runs a Simple Moving Average (SMA) algorithim on the stock ticker provided.
    The short term and long terma rolling means can be adjusted to create a Dual Moving
    Average (DMA) model
"""

import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
import constants
import datetime
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None  # default='warn'


api = tradeapi.REST(
    constants.API_KEY,
    constants.API_SECRET_KEY,
    constants.MARKET
)

date = datetime.datetime.now()
start = (date - datetime.timedelta(days=300)).strftime("%Y-%m-%d")

def maModel(ticker):
    # get daily stock data for the ticker provided
    tickerdata = api.get_bars(ticker, TimeFrame.Day,start=start).df
    day = np.arange(1, len(tickerdata) + 1)
    tickerdata['day']= day

    # Calculate rolling averages per day
    tickerdata['short-term'] = tickerdata['close'].rolling(5).mean()
    tickerdata['long-term'] = tickerdata['close'].rolling(25).mean()

    # add a signal for buy or sell
    tickerdata['signal'] = np.where(tickerdata['short-term'] > tickerdata['long-term'], 1, 0)
    tickerdata['signal'] = np.where(tickerdata['short-term'] < tickerdata['long-term'], -1, tickerdata['signal'])
    tickerdata.dropna(inplace=True)

    # create a flag for when to create buy or sell transaction
    tickerdata['return'] = np.log(tickerdata['close']).diff()
    tickerdata['system_return'] = tickerdata['signal'] * tickerdata['return']
    tickerdata['transactionFlag'] = tickerdata.signal.diff()
    
    return tickerdata.loc[tickerdata.index[-1],'transactionFlag']

def maChannelModel(ticker):
    # get daily stock data for the ticker provided
    tickerdata = api.get_bars(ticker, TimeFrame.Day, limit=300).df
    day = np.arange(1, len(tickerdata) + 1)
    tickerdata['day']= day

    # Calculate rolling averages per day
    tickerdata['short-term'] = tickerdata['high'].rolling(10).mean()
    tickerdata['long-term'] = tickerdata['low'].rolling(10).mean()
    tickerdata['prev-close'] = tickerdata['close'].shift()
    tickerdata['prev-short'] = tickerdata['short-term'].shift()
    tickerdata['prev-long'] = tickerdata['long-term'].shift()
    
    # add a signal for buy or sell
    tickerdata['signal'] = np.where(((tickerdata['close'] > tickerdata['short-term']) & (tickerdata['prev-close'] > tickerdata['prev-short'])), 1, 0)
    tickerdata['signal'] = np.where(((tickerdata['close'] < tickerdata['long-term']) & (tickerdata['prev-close'] < tickerdata['prev-long'])), -1, tickerdata['signal'])
    tickerdata.dropna(inplace=True)

    # create a flag for when to create buy or sell transaction
    tickerdata['return'] = np.log(tickerdata['close']).diff()
    tickerdata['system_return'] = tickerdata['signal'] * tickerdata['return']
    tickerdata['transactionFlag'] = tickerdata.signal.diff()
    
    print(tickerdata['return'])
    # maPlot(tickerdata)
    
    return tickerdata.loc[tickerdata.index[-1],'transactionFlag']


###################################################
# Functions maPlot and maPerformance              #
# are strictly for testing and research purposes  #
###################################################

# def maPlot(gld):
#     plt.rcParams['figure.figsize'] = 12, 6
#     plt.grid(True, alpha = .3)
#     plt.plot(gld.iloc[-208:]['close'], label = 'GLD')
#     plt.plot(gld.iloc[-208:]['short-term'], label = 'short-term')
#     plt.plot(gld.iloc[-208:]['long-term'], label = 'long-term')
#     plt.plot(gld[-208:].loc[gld.transactionFlag == 2].index, gld[-208:]['short-term'][gld.transactionFlag == 2], '^',
#            color = 'g', markersize = 12)
#     plt.plot(gld[-208:].loc[gld.transactionFlag == -2].index, gld[-208:]['long-term'][gld.transactionFlag == -2], 'v',
#             color = 'r', markersize = 12)
#     plt.legend(loc=2)
#     plt.show()

# def maPerformance(gld):
#     plt.plot(np.exp(gld['return']).cumprod(), label='Buy/Hold')
#     plt.plot(np.exp(gld['system_return']).cumprod(), label='System')
#     plt.legend(loc=2)
#     plt.grid(True, alpha=.3)
#     plt.show()
    


