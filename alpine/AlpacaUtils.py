"""
    File name: main.py
    Author: Timothy Clark
    Date created: 6/27/2021
    Date last modified: 6/27/2021
    Python Version: 3.8

    Description: this file contains all utility methods used when connecting to the Alpaca API
"""

import alpaca_trade_api as tradeapi
import constants
import datetime
import pandas as pd

api = tradeapi.REST(
    constants.API_KEY,
    constants.API_SECRET_KEY,
    constants.MARKET
)

def isTomorrowOpen():
    result = False
    date = datetime.datetime.now() + datetime.timedelta(1)
    tomorrow = date.strftime("%Y-%m-%d %H:%M:%S")
    calendar = api.get_calendar(tomorrow,tomorrow)[0]

    if str(calendar.date)[:10] == tomorrow[:10]:
        result = True

    print(result)
    return result

def isTodayOpen():
    result = False
    date = datetime.datetime.now()
    today = date.strftime("%Y-%m-%d %H:%M:%S")
    calendar = api.get_calendar(today, today)[0]

    if str(calendar.date)[:10] == today[:10]:
        result = True

    print(result)
    return result

def createTransaction(symbol, qty, side, type, tif):
    api.submit_order(symbol,qty,side,type,tif)

def getHistory():
    history= api.get_portfolio_history(period='1W', timeframe='1H',).df
    return history.drop(columns=['profit_loss', 'profit_loss_pct'])

def getEquity():
    account = api.get_account()

    equity = account.equity

    return "$"+str(equity)
