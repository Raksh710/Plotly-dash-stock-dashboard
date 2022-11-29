import numpy as np
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly import tools
import dash, json
from dash import dcc, html, Dash
from dash.dependencies import Input, Output, State
import base64
import requests

import pandas_datareader as web
from datetime import datetime
import yfinance as yf

nsdq = pd.read_csv('NASDAQcompanylist.csv')
nsdq.set_index('Symbol',inplace=True)
#nsdq

app = Dash()
options=[]
options = [{'label':f"{tic} {nsdq.loc[tic]['Name']}" , 'value':tic} for tic in nsdq.index]

app.layout = html.Div([
    html.H1('Stock Ticker Dashboard'),
    html.Div([
        html.H3('Select the Stock Symbols: ', style={'paddingRight':'30px','border':'1px green solid'}),
        dcc.Dropdown(id='my-ticker-symbol', options=options, value=['TSLA'], multi=True, style={'border':'1px blue solid'})
    ], style={'display':'inline-block','verticalAlign':'top', 'width':'28%','border':'1px green solid'}),
    html.Div([
        html.H3('Select start and end dates: '),
        dcc.DatePickerRange(id='my-date-range', min_date_allowed=datetime(2000,1,1), max_date_allowed = datetime.today(), start_date = datetime(2001,1,1), end_date=datetime.today())
    ], style={'display':'inline-block'}),
    html.Div([
        html.Button(id='submit-button',n_clicks=0,children='Submit',style={'fontSize':24,'marginLeft':'30px'}),
    ], style={'display':'inline-block'}),
    dcc.Graph(id='my-graph', figure={'data':[{'x':[1,2] , 'y':[3,4] } ] } ),
    html.Div([
        html.H4(id='sharpe-ratio')
    ])

], style={'border':'4px blue solid'})

@app.callback(Output('my-graph','figure'),[Input('submit-button','n_clicks')], [State('my-ticker-symbol','value'), State('my-date-range','start_date'), State('my-date-range','end_date')])
def update_graph(n_clicks,stock_ticker,start_date,end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    traces=[]
    for tic in stock_ticker:
        df = yf.download(tic,start=start,end=end)
        traces.append({'x':df.index,'y':df['Adj Close'], 'name':tic})
    fig = {'data':traces, 'layout': {'title':', '.join(stock_ticker) + ' Closing Prices' , 'hovermode':'closest'}}
    return fig

#@app.callback(Output('sharpe-ratio','children'),[Input('submit-button','n_clicks')], [State('my-ticker-symbol','value'), State('my-date-range','start_date'), State('my-date-range','end_date')])
#def show_sr(n_clicks,stock_ticker,start_date,end_date):
#    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
#    end= datetime.strptime(end_date[:10], '%Y-%m-%d')
#    sr=[]
#    for tic in stock_ticker:
#        df = yf.download(tic,start,end)
#        sharpe_ratio = df['Adj Close'].mean()/df['Adj Close'].std()
#        sr.append(f" The sharpe ratio for {tic} from {start} to {end} is {round(sharpe_ratio,2)} ")
#    return ' '.join(sr)


if __name__=='__main__':
    app.run_server()