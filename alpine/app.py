
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output
import AlpacaUtils
import sqlUtils
import constants
import movingAverage
import logging
from apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig(filename='alpine.log', level=logging.INFO)
logging.info('app started')
def runAlgorithm():
    if AlpacaUtils.isTomorrowOpen():
        stocks = sqlUtils.getPortfolio()
        logging.info(stocks)
        analysis=[]
        for index, stock in stocks.iterrows():
            # replace tradingAlgorithms method to run analysis using different approaches
            logging.info("analyzing " + stock['symbol'])
            stockAnalysis = movingAverage.maModel(stock['symbol'])
            logging.info(stockAnalysis)
            analysis.append(stockAnalysis)
        if stockAnalysis == 2.0:
            sqlUtils.createBuy(stock[1], 2)
        elif stockAnalysis == -2.0:
            sqlUtils.createSell(stock[1])
        stocks['analysis']=analysis
        
        
def postTransactions():
    if AlpacaUtils.isTodayOpen():
        transactions = sqlUtils.getTransactions()
        logging.info(transactions)
        if transactions:
            for trans in transactions:
                AlpacaUtils.createTransaction(trans[1], trans[2], trans[3], trans[4], trans[5])
                sqlUtils.deleteTransaction(trans[0])
                sqlUtils.updatePortfolio(trans[6],trans[3])

    
scheduler = BackgroundScheduler()
scheduler.add_job(runAlgorithm, 'cron', minute='30', hour='09', day_of_week='mon-fri', month ='*', year='*', timezone='utc')
scheduler.add_job(postTransactions, 'cron', minute='00', hour='10', day_of_week='mon-fri', month ='*', year='*', timezone='utc')
scheduler.start()

# intialize
app = dash.Dash(__name__,
external_stylesheets =[dbc.themes.DARKLY])
# define
app.config.update(result_expires=3600,
                enable_utc = True,
                timezone = 'UTC')

app.layout = html.Div([
    html.Div([
        html.Img(src="/assets/Alpine 2.png", style={'height':'10%', 'width':'10%'}),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Portfolio", style={'color': 'primary'}),
                dbc.CardBody([
                    html.H2(id="portfolioValue",style={"color":"primary"}),
                    dcc.Graph(id="historyGraph",),
                    dcc.Interval(
                        id='graphInterval',
                        interval=60 * 1000,  # in milliseconds
                        n_intervals=0
                    )
                ])
            ],style={"height":"100%"})
        ],width=9),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Queued Transactions", style={'color': 'primary'}),
                dbc.CardBody([

                ],id='transactionCard'),
                dcc.Interval(id='transactionInterval',
                        interval=35 * 1000,  # in milliseconds
                        n_intervals=0
                    )
            ],style={"height":"100%"})
        ],width=3)
    ])
])

@app.callback(Output('historyGraph','figure'),
              Output('portfolioValue','children'),
              Input('graphInterval','n_intervals'))
def updateGraph(n):
    historyData = AlpacaUtils.getHistory()

    histFigure = go.Figure(data=[go.Scatter(x=historyData.index, y=historyData['equity'],line=dict(color="#13ebbd"))],
                           layout=go.Layout(template="plotly_dark"))

    value = AlpacaUtils.getEquity()
    return histFigure, value


@app.callback(Output('transactionCard','children'),
              Input('transactionInterval','n_intervals'))
def updateList(n):
    transactionTable = sqlUtils.getTransactions().drop(columns=['trans_id', 'type', 'time_in_force'])
    table = dbc.Table.from_dataframe(transactionTable,striped=False, bordered=True, hover=True)


    return table


# run
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)