import AlpacaUtils
import sqlUtils
import os
from apscheduler.schedulers.background import BackgroundScheduler


def printTest():
    print('scheduler is working')

def runAlgorithm():
    if AlpacaUtils.isTomorrowOpen():
        stocks = sqlUtils.getPortfolio()
        print(stocks)
        for index, stock in stocks.iterrows():
            # replace tradingAlgorithms method to run analysis using different approaches
            app.logger.info("analyzing " + stock['symbol'])
            stockAnalysis = movingAverage.maModel(stock['symbol'])
            app.logger.info(stockAnalysis)
        if stockAnalysis == 2.0:
            sqlUtils.createBuy(stock[1], 2)
        elif stockAnalysis == -2.0:
            sqlUtils.createSell(stock[1])

    string ="running algorithm"
    return string


def postTransactions():
    if AlpacaUtils.isTodayOpen():
        transactions = sqlUtils.getTransactions()
        for trans in transactions:
            AlpacaUtils.createTransaction(trans[1], trans[2], trans[3], trans[4], trans[5])
            sqlUtils.deleteTransaction(trans[0])
            sqlUtils.updatePortfolio(trans[6])
    string ="posting transaction"
    return string

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(printTest, 'cron', minute='17', hour='01', day='*', month ='*', year='*', timezone='utc')
    scheduler.start()
    input('press Enter to stop')
    scheduler.shutdown()