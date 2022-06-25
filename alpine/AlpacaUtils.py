"""
    File name: main.py
    Author: Timothy Clark
    Date created: 6/27/2021
    Date last modified: 05/29/2022
    Python Version: 3.9

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
    date = datetime.datetime.now() + datetime.timedelta(days=1)
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
    api.submit_order(symbol=symbol,qty=qty,side=side,type=type,time_in_force=tif)

def getHistory():
    history= api.get_portfolio_history(period='1W', timeframe='1H').df
    return history.drop(columns=['profit_loss', 'profit_loss_pct'])

def getEquity():
    account = api.get_account()

    equity = account.equity

    return "$"+str(equity)

def getWatchlist():
    watchlist = api.get_watchlist(constants.WATCHLIST_ID)
    stocks=[]
    for company in watchlist.assets:
        stocks.append(company['symbol'])
    
    stockString = ','.join(stocks)

    return stockString

def getStockNews(stocks):
    startDate = datetime.datetime.now()- datetime.timedelta(days=2)
    startDate = startDate.strftime("%Y-%m-%dT%H:%M:%SZ")
    news =api.get_news(symbol=stocks,start=startDate, limit=25, include_content= True, exclude_contentless=True)

    return news







