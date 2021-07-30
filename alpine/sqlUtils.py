
"""
    File name: movingAverage.py
    Author: Timothy Clark
    Date created: 6/26/2021
    Date last modified: 7/10/2021
    Python Version: 3.8

    Description: accesses SQLite3 database to create a transaction object to be processed
"""
import sqlite3
import pandas as pd
import constants

# setup sqlite3 connection and cursor

connection = sqlite3.connect(constants.SQL_DB_NAME)
cursor = connection.cursor()

# Create table for initial build

createTransactionTableCommand = """CREATE TABLE IF NOT EXISTS
transactions(trans_id INTEGER PRIMARY KEY AUTOINCREMENT, symbol TEXT, side TEXT, qty INTEGER, type TEXT, time_in_force TEXT, port_id INTEGER NOT NULL,
FOREIGN KEY (port_id) REFERENCES portfolio (port_id));"""
createPortfolioTableCommand = """CREATE TABLE IF NOT EXISTS
portfolio(port_id INTEGER PRIMARY KEY AUTOINCREMENT, symbol TEXT, qty INTEGER );"""


cursor.execute(createTransactionTableCommand)
cursor.execute(createPortfolioTableCommand)
connection.commit()
cursor.close()
connection.close()

# Create a buy transaction
def createBuy(ticker, qty):
    connection = sqlite3.connect(constants.SQL_DB_NAME)
    cursor = connection.cursor()
    portCommand = """SELECT port_id FROM portfolio WHERE symbol = ? """
    selectQuery = cursor.execute(portCommand, (ticker,)).fetchone()
    port_id = selectQuery[0]
    values =(ticker,qty, port_id)
    buyCommand = """INSERT INTO transactions(symbol,side,qty,type,time_in_force, port_id)
     VALUES(?,'buy',?,'market','opg',?);"""

    cursor.execute(buyCommand,values)
    connection.commit()
    cursor.close()
    connection.close()

# create a sell transaction
def createSell(ticker):
    connection = sqlite3.connect(constants.SQL_DB_NAME)
    cursor = connection.cursor()
    portCommand = """SELECT port_id, qty FROM portfolio WHERE symbol = ? """
    selectQuery = cursor.execute(portCommand, (ticker,)).fetchone()
    port_id = selectQuery[0]
    qty = selectQuery[1]
    values =(ticker, qty, port_id)
    sellCommand = """INSERT INTO transactions(symbol,side,qty,type,time_in_force,port_id)
     VALUES(?,'Sell',?,'market','opg',?);"""

    cursor.execute(sellCommand,values)
    connection.commit()
    cursor.close()
    connection.close()

# get a list of transactions in the sqlite db
def getTransactions():
    connection = sqlite3.connect(constants.SQL_DB_NAME)
    selectAllCommand ="""SELECT * FROM transactions;"""
    transactions = pd.read_sql_query(selectAllCommand, connection)
    connection.close()
    return transactions

def getPortfolio():
    connection = sqlite3.connect(constants.SQL_DB_NAME)
    portfolioCommand = """SELECT * from portfolio;"""
    portfolio = pd.read_sql_query(portfolioCommand,connection)
    connection.close()
    return portfolio

def addStock(ticker,qty):
    connection = sqlite3.connect(constants.SQL_DB_NAME)
    cursor = connection.cursor()
    values = (ticker, qty)
    sellCommand = """INSERT INTO portfolio(symbol,qty)
        VALUES(?,?);"""

    cursor.execute(sellCommand, values)
    connection.commit()
    cursor.close()
    connection.close()

def deleteTransaction(trans_id):
    connection = sqlite3.connect(constants.SQL_DB_NAME)
    cursor = connection.cursor()
    deleteCommand = """DELETE FROM transactions WHERE trans_id = ?;"""
    cursor.execute(deleteCommand,(trans_id,))
    connection.commit()
    cursor.close()
    connection.close()

def updatePortfolio(port_id, qty):
    connection = sqlite3.connect(constants.SQL_DB_NAME)
    cursor = connection.cursor()
    updateCommand= "UPDATE portfolio SET qty = ? WHERE port_id = ?;"
    cursor.execute(updateCommand, (qty, port_id))
    connection.commit()
    cursor.close()
    connection.close()


