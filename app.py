# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 10:44:35 2020

@author: HanaFI
"""


import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_table
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

from VaRTest import main, Returns

df = main()
Ret = Returns(Selection = True)
Correl = Ret.corr().reset_index() # round(Ret[[x for x in Ret.columns if "2" in x]][-252:].corr(), 2).reset_index()

Liste = sorted(list(set([''.join([z for z in x if z.isdigit() is False]) for x in Ret.columns])))


def generate_table(dataframe):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(len(dataframe))
        ])
    ])

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Risk Metrics', children=[
            html.H4(children='Value at Risk and MaxDrawdown'),
            dash_table.DataTable(
                id='table1',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                style_table={'overflowX': 'scroll'},
                style_cell={ 'minWidth': '0px', 'maxWidth': '50px', },
                )
        ]),
        dcc.Tab(label='Correlation', children=[
            html.H4(children='Correlation for the First contract'),
            
            html.Div([
                html.H6(children='Choosing Maturity:', style={'display': 'inline-block'}),
                dcc.Dropdown(
                    id='FutureMaturity',
                    options=[{'label': i, 'value': i} for i in range(1,5)],
                    value="1",
                    style={'width': '49%', 'display': 'inline-block'},
                    )
                ]),
            
            dash_table.DataTable(
                id='Correltable',
                data=Correl.to_dict('records'),
                columns=[{"name": i, "id": i} for i in Correl.columns],
                style_table={'overflowX': 'scroll'},
                style_cell={ 'minWidth': '0px', 'maxWidth': '50px'},
                ),
            

            
            html.Div([ html.H4(children="Change Window Size:", style={'display': 'inline-block' }),
                dcc.Input(id='CorrWindow', value=252, debounce=True)]),
            
            dcc.Graph(id='RollingCorrel')
        ]),
        dcc.Tab(label='Backtest', children=[
            
            
            html.Div(html.Br()),
            
            html.Div( className='row', style = {'display' : 'inline-flex', 'position': 'relative'},
                children=[
                        html.Div([dcc.Input(id="CommoWeight1", value = 1, type='number', style={'width':'25%', 'position': 'absolute', 'bottom': '0','margin-left': '0px'})]),
                        html.Div([ html.Label(["Pick a Commo:", dcc.Dropdown(id="CommoPick1", options=[{'label':x, 'value':x} for x in Liste], value="BO",style={'width': '100%'}  )])], style={'margin-left': '75px'}),
                        html.Div([ html.Label(["Pick a Maturity:", dcc.Dropdown(id="MaturityPick1", options=[{'label':str(x), 'value':str(x)} for x in range(1,5)], value="1",style={'width': '100%'} )])], style={'margin-left': '5px'} ),
            ]),
            
            html.Div( className='row', style = {'display' : 'inline-flex', 'position': 'relative','margin-left': '100px'},
                children=[
                        html.Div([dcc.Input(id="CommoWeight2", value = 0, type='number', style={'width':'25%', 'position': 'absolute', 'bottom': '0','margin-left': '0px'})]),
                        html.Div([ html.Label(["Pick a Commo:", dcc.Dropdown(id="CommoPick2", options=[{'label':x, 'value':x} for x in Liste], value="BO",style={'width': '100%'}  )])], style={'margin-left': '75px'}),
                        html.Div([ html.Label(["Pick a Maturity:", dcc.Dropdown(id="MaturityPick2", options=[{'label':str(x), 'value':str(x)} for x in range(1,5)], value="1",style={'width': '100%'} )])], style={'margin-left': '5px'} ),
            ]),

            dcc.Graph(id="ReturnsGraph"),
            
            dcc.Graph(id="ACF"),
            

            
        ]),
    ])
])





@app.callback(
    Output("ReturnsGraph", "figure"),
    [Input("CommoWeight1", "value"), Input("CommoPick1", "value"), Input("MaturityPick1", "value"), Input("CommoWeight2", "value"), Input("CommoPick2", "value"), Input("MaturityPick2", "value")])
def update_graph(Weight1, Commo1, Maturity1, Weight2, Commo2, Maturity2):
    Title = ""
    if Weight1 is None:
        Weight1 = 0
    if Weight2 is None:
        Weight2 = 0
    if Weight1 != 0: Title = Title + Commo1
    if Weight2 != 0: Title = Title + Commo2
    if len(Title) > 2: Title = Title[:2] +" & " + Title[2:]
    df = Weight1 * Ret[Commo1+Maturity1] + Weight2 * Ret[Commo2+Maturity2]
    df = df+1
    df.iloc[0] = 100   
  
    return {
        'data': [    dict(x= pd.to_datetime(df.index, format="%Y%m%d") , 
                          y= [x for x in df.cumprod()], 
                          name= 'Cumulated Returns')
                 ],
        'layout': dict(title='Returns of ' + Title)
        }

@app.callback(
    Output("ACF", "figure"),
    [Input("CommoWeight1", "value"), Input("CommoPick1", "value"), Input("MaturityPick1", "value"), Input("CommoWeight2", "value"), Input("CommoPick2", "value"), Input("MaturityPick2", "value")])
def update_graph2(Weight1, Commo1, Maturity1, Weight2, Commo2, Maturity2):
    Title = ""
    if Weight1 is None:
        Weight1 = 0
    if Weight2 is None:
        Weight2 = 0
    if Weight1 != 0: Title = Title + Commo1
    if Weight2 != 0: Title = Title + Commo2
    if len(Title) > 2: Title = Title[:2] +" & " + Title[2:]
    df = Weight1 * Ret[Commo1+Maturity1] + Weight2 * Ret[Commo2+Maturity2]
    ACFListe = []
    for x in range(60):
        ACFListe.append( pd.concat((df, df.shift(x)), axis=1).dropna().corr().iloc[0,1] )
    return {
        'data': [    dict(x= [x for x in range(len(ACFListe))] , 
                          y= [x for x in ACFListe], 
                          type= 'bar',
                          
                          name= 'Cumulated Returns')
                 ],
        'layout': dict(title='AutoCorrelation Function',
                       xaxis={'tickmode':'linear'},)
        }

 
@app.callback(
    [Output('Correltable', 'data'), Output('Correltable', 'columns')],
    [Input('FutureMaturity', "value")])
def update_table(value):
    Correl = round(Ret[[x for x in Ret.columns if str(value) in x]][-252:].corr(), 2).reset_index()
    data=Correl.to_dict('records')
    columns=[{"name": i, "id": i} for i in Correl.columns]
    return (data, columns)
        
    
@app.callback(
    Output('RollingCorrel', 'figure'),
    [Input('Correltable', 'active_cell'), Input('Correltable', 'data'), Input('CorrWindow', 'value')])
def update_graph1(X1, X2, Window):
    if X1 is None:
        return {'data':[dict(x=[0,1,2], y=[0,0,0])],'layout':dict(title='Please select a correlation pairs')}
    elif X1["column_id"] == "index":
        return {'data':[dict(x=[0,1,2], y=[0,0,0])],'layout':dict(title='Please select a correlation pairs')}
    elif int(Window) < 0 or int(Window) > len(Ret):
        return {'data':[dict(x=[0,1,2], y=[0,0,0])],'layout':dict(title='Please select a correlation pairs')}
    else:
        X2 = X2[X1['row']]['index']
        X1 = X1["column_id"]
        Window = int(Window)
    
        return {
            'data': [    dict(x= pd.to_datetime(Ret.index[Window:], format="%Y%m%d") , 
                              y= [Ret[[X2, X1]].iloc[z:z+Window].corr().iloc[0,1] for z in range(len(Ret)-Window) ] )
                ],
            'layout': dict(title='Correlation between ' + X1 + " and " + X2 + " (Window size:" + str(Window) +" Days)")
            
            }

    

if __name__ == '__main__':
    app.run_server(debug=True)