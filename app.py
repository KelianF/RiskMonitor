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
            
            # html.Div(id='Test'),
            
            html.Div([ html.H4(children="Change Window Size:", style={'display': 'inline-block' }),
                dcc.Input(id='CorrWindow', value=252, debounce=True)]),
            
            dcc.Graph(id='RollingCorrel')
        ]),
        dcc.Tab(label='Here, we can add some more stuff', children=[
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [2, 4, 3],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [5, 4, 3],
                         'type': 'bar', 'name': u'Montréal'},
                    ]
                }
            )
        ]),
    ])
])

 
@app.callback(
    [Output('Correltable', 'data'), Output('Correltable', 'columns')],
    [Input('FutureMaturity', "value")])
def update_table(value):
    Correl = round(Ret[[x for x in Ret.columns if str(value) in x]][-252:].corr(), 2).reset_index()
    data=Correl.to_dict('records')
    columns=[{"name": i, "id": i} for i in Correl.columns]
    return (data, columns)
        
# @app.callback(
#     Output('Test', 'children'),
#     [Input('Correltable', 'active_cell'), Input('Correltable', 'data'), Input('CorrWindow', 'value')])
# def update_output_div(value, df, Window):
#     if value is None:
#         return "Click Something"
#     else:
#         row = df[value['row']]['index']
#         col = value["column_id"]
#         return ' \n You\'ve entered "{}" et "{}" with window of {} '.format(row, col, Window)


    
@app.callback(
    Output('RollingCorrel', 'figure'),
    [Input('Correltable', 'active_cell'), Input('Correltable', 'data'), Input('CorrWindow', 'value')])
def update_graph(X1, X2, Window):
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