
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

from dash.dependencies import Input, Output
from celeryconfig import make_celery
import AlpacaUtils
import sqlUtils
import constants
import movingAverage

# intialize
app = dash.Dash(__name__,
external_stylesheets =[dbc.themes.DARKLY])
# define
app.config.update(CELERY_BROKER_URL=constants.CELERY_BROKER_URL,
                CELERY_RESULT_BACKEND=constants.CELERY_RESULT_BACKEND)
app.config.update(result_expires=3600,
                enable_utc = True,
                timezone = 'UTC')

celery = make_celery(app, __name__)
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
    # transactionTable = pd.DataFrame(
    # {
    #     "symbol": ["Arthur", "Ford", "Zaphod", "Trillian"],
    #     "type": ["buy", "sell", "buy", "buy"],
    # })
    # for index, row in transactionTable.iterrows():
    #     if row['type'] == 'buy':
    #         row['type'] = '<i class="bi bi-caret-up-fill"></i>'
    #     elif row['type'] =='sell':
    #         row['type'] = '<i class="bi bi-caret-up-fill"></i>'

    table = dbc.Table.from_dataframe(transactionTable,striped=False, bordered=True, hover=True)


    return table

@celery.task(name='app.runAlgorithm')
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

@celery.task(name='app.postTransactions')
def postTransactions():
    if AlpacaUtils.isTodayOpen():
        transactions = sqlUtils.getTransactions()
        for trans in transactions:
            AlpacaUtils.createTransaction(trans[1], trans[2], trans[3], trans[4], trans[5])
            sqlUtils.deleteTransaction(trans[0])
            sqlUtils.updatePortfolio(trans[6])
    string ="posting transaction"
    return string
# run
if __name__ == '__main__':
    app.run_server(debug=True)
