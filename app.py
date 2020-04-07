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
import numpy as np

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
            
            dcc.RadioItems(id="ChoiceCorrelType", value="Mat", options=[{'label':'By Maturities', "value": "Mat"}, {"label":"By Commodities", "value":"Commo"}]),
            
            html.Div([
                html.H6(children='Choice:', style={'display': 'inline-block'}),
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
            

            
            html.Div([ html.H5(children="Change Window Size:", style={'display': 'inline-block' }),
                dcc.Input(id='CorrWindow', value=252, debounce=True)]),
            
            dcc.Graph(id='RollingCorrel')
        ]),
            
        dcc.Tab(label='Backtest', children=[
            
            
            html.Div(html.Br()),
            
            html.Div([
            html.Button("More",id="MoreCommos", n_clicks=0),
            html.Button("Less",id="LessCommos", n_clicks=0),
            ]),
            
            html.Div(html.Br()),
            
            html.Div( className='row', style = {'display' : 'inline-flex', 'position': 'relative'},
                children=[
                        html.Div([dcc.Input(id="CommoWeight1", value = 1, type='number', style={'width':'25%', 'position': 'absolute', 'bottom': '0','margin-left': '0px'})]),
                        html.Div([ html.Label(["Pick a Commo:", dcc.Dropdown(id="CommoPick1", options=[{'label':x, 'value':x} for x in Liste], value="BO",style={'width': '100%'}  )])], style={'margin-left': '75px'}),
                        html.Div([ html.Label(["Pick a Maturity:", dcc.Dropdown(id="MaturityPick1", options=[{'label':str(x), 'value':str(x)} for x in range(1,5)], value="1",style={'width': '100%'} )])], style={'margin-left': '5px'} ),
            ]),
            
            html.Div(id="CommoInput2", className='row', style = {'display': 'none' },
                children=[
                        html.Div([dcc.Input(id="CommoWeight2", value = 0, type='number', style={'width':'25%', 'position': 'absolute', 'bottom': '0','margin-left': '0px'})]),
                        html.Div([ html.Label(["Pick a Commo:", dcc.Dropdown(id="CommoPick2", options=[{'label':x, 'value':x} for x in Liste], value="BO",style={'width': '100%'}  )])], style={'margin-left': '75px'}),
                        html.Div([ html.Label(["Pick a Maturity:", dcc.Dropdown(id="MaturityPick2", options=[{'label':str(x), 'value':str(x)} for x in range(1,5)], value="1",style={'width': '100%'} )])], style={'margin-left': '5px'} ),
            ]),
            
            html.Div(html.Br()),
            
            html.Div(id="CommoInput3", className='row', style={'display': 'none'},
                children=[
                        html.Div([dcc.Input(id="CommoWeight3", value = 0, type='number', style={'width':'25%', 'position': 'absolute', 'bottom': '0','margin-left': '0px'})]),
                        html.Div([ html.Label(["Pick a Commo:", dcc.Dropdown(id="CommoPick3", options=[{'label':x, 'value':x} for x in Liste], value="BO",style={'width': '100%'}  )])], style={'margin-left': '75px'}),
                        html.Div([ html.Label(["Pick a Maturity:", dcc.Dropdown(id="MaturityPick3", options=[{'label':str(x), 'value':str(x)} for x in range(1,5)], value="1",style={'width': '100%'} )])], style={'margin-left': '5px'} ),
            ]),
            
            html.Div(id="CommoInput4", className='row', style={'display': 'none'},
                children=[
                        html.Div([dcc.Input(id="CommoWeight4", value = 0, type='number', style={'width':'25%', 'position': 'absolute', 'bottom': '0','margin-left': '0px'})]),
                        html.Div([ html.Label(["Pick a Commo:", dcc.Dropdown(id="CommoPick4", options=[{'label':x, 'value':x} for x in Liste], value="BO",style={'width': '100%'}  )])], style={'margin-left': '75px'}),
                        html.Div([ html.Label(["Pick a Maturity:", dcc.Dropdown(id="MaturityPick4", options=[{'label':str(x), 'value':str(x)} for x in range(1,5)], value="1",style={'width': '100%'} )])], style={'margin-left': '5px'} ),
            ]),
            
            html.Div(html.Br()),
            
            html.Div(id="CommoInput5", className='row', style={'display': 'none'},
                children=[
                        html.Div([dcc.Input(id="CommoWeight5", value = 0, type='number', style={'width':'25%', 'position': 'absolute', 'bottom': '0','margin-left': '0px'})]),
                        html.Div([ html.Label(["Pick a Commo:", dcc.Dropdown(id="CommoPick5", options=[{'label':x, 'value':x} for x in Liste], value="BO",style={'width': '100%'}  )])], style={'margin-left': '75px'}),
                        html.Div([ html.Label(["Pick a Maturity:", dcc.Dropdown(id="MaturityPick5", options=[{'label':str(x), 'value':str(x)} for x in range(1,5)], value="1",style={'width': '100%'} )])], style={'margin-left': '5px'} ),
            ]),
            
            html.Div(id="CommoInput6", className='row', style={'display': 'none'},
                children=[
                        html.Div([dcc.Input(id="CommoWeight6", value = 0, type='number', style={'width':'25%', 'position': 'absolute', 'bottom': '0','margin-left': '0px'})]),
                        html.Div([ html.Label(["Pick a Commo:", dcc.Dropdown(id="CommoPick6", options=[{'label':x, 'value':x} for x in Liste], value="BO",style={'width': '100%'}  )])], style={'margin-left': '75px'}),
                        html.Div([ html.Label(["Pick a Maturity:", dcc.Dropdown(id="MaturityPick6", options=[{'label':str(x), 'value':str(x)} for x in range(1,5)], value="1",style={'width': '100%'} )])], style={'margin-left': '5px'} ),
            ]),
            
            
            # html.Div(id="Test0"),
            
            dcc.Graph(id="ReturnsGraph"),
            
            
            
            dcc.Graph(id="CorrelGraph", style={'display':'block'}),
            html.Div(id="DivSliderWindowCorrel", children=[dcc.Slider(id="SliderWindowCorrel",value = 252, min=5, max=252, marks= {str(x): str(x) for x in [5,10,20,40,60,80,100,200,252]}, step=None,)], ),
            html.Br(),
            dcc.Graph(id="ACF"),
            
        ]),
    ])
])


# @app.callback(
#     Output("Test0", "children"),
#     [Input("ReturnsGraph", "relayoutData")])
# def update_Test(Val):
#     if Val is not None:
#         if 'xaxis.range[0]' in Val.keys():
#             return Val['xaxis.range[0]'].split(" ")[0]
#     else:
    
#         return str(Val)



@app.callback(
    [Output("FutureMaturity", "value"), Output("FutureMaturity", "options")],
    [Input("ChoiceCorrelType", "value")])
def update_Dropdown(Value):
    if Value=="Mat": return "1", [{'label': i, 'value': i} for i in range(1,5)]
    else: return "BO", [{'label': i, 'value': i} for i in Liste]




@app.callback(
    [Output("CorrelGraph", "figure"),Output("CorrelGraph", "style"),Output("DivSliderWindowCorrel", "style")],
    [Input("CommoWeight1", "value"), Input("CommoPick1", "value"), Input("MaturityPick1", "value"), Input("CommoWeight2", "value"), Input("CommoPick2", "value"), Input("MaturityPick2", "value"),
     Input("CommoWeight3", "value"), Input("CommoPick3", "value"), Input("MaturityPick3", "value"), Input("CommoWeight4", "value"), Input("CommoPick4", "value"), Input("MaturityPick4", "value"),
     Input("CommoWeight5", "value"), Input("CommoPick5", "value"), Input("MaturityPick5", "value"), Input("CommoWeight6", "value"), Input("CommoPick6", "value"), Input("MaturityPick6", "value"),
     Input("SliderWindowCorrel", "value"), Input("ReturnsGraph", "relayoutData"),
     ])
def update_graph(Weight1, Commo1, Maturity1, Weight2, Commo2, Maturity2, Weight3, Commo3, Maturity3, Weight4, Commo4, Maturity4, Weight5, Commo5, Maturity5, Weight6, Commo6, Maturity6, Window, Date):
    if Weight1 is None: Weight1 = 0
    if Weight2 is None: Weight2 = 0
    if Weight3 is None: Weight3 = 0
    if Weight4 is None: Weight4 = 0
    if Weight5 is None: Weight5 = 0
    if Weight6 is None: Weight6 = 0
    
    if Commo1 not in Liste or Commo2 not in Liste or Commo3 not in Liste or Commo4 not in Liste or Commo5 not in Liste or Commo6 not in Liste: return dash.no_update, dash.no_update, dash.no_update
    
    
    
    df1 = Weight1*Ret[Commo1+Maturity1] +  Weight3*Ret[Commo3+Maturity3] + Weight5*Ret[Commo5+Maturity5]
    
    df2 = Weight2*Ret[Commo2+Maturity2] + Weight4*Ret[Commo4+Maturity4] + Weight6*Ret[Commo6+Maturity6]
    df = pd.concat((df1, df2), axis=1)
    if Date is not None: 
        if 'xaxis.range[0]' in Date.keys(): 
            df = df[(df.index >= int(Date['xaxis.range[0]'].split(" ")[0].replace("-",""))) & (df.index <= int(Date['xaxis.range[1]'].split(" ")[0].replace("-","")))]
    Window = int(Window)
    
    if Weight2==0 and Weight4==0 and Weight6==0: return {'data':[dict(x=[0,1,2], y=[0,0,0])],'layout':dict(title='Please select a correlation pairs')}, {'display':'none'}, {'display':'none'}
    
    else:
        return {
            'data': [    dict(x= pd.to_datetime(df.index[Window:], format="%Y%m%d") , 
                              y= [df.iloc[z:z+Window].corr().iloc[0,1] for z in range(len(df)-Window) ] )
                ],
            'layout': dict(title='Correlation (Left Vs. Right Commodities)')
            
            }, {}, {"width":"50%"}




@app.callback(
    [Output('CommoInput2', 'style'), Output('CommoInput3', 'style'), Output('CommoInput4', 'style'), Output('CommoInput5', 'style'), Output('CommoInput6', 'style'),
     Output('CommoWeight2', 'value'), Output('CommoWeight3', 'value'), Output('CommoWeight4', 'value'), Output('CommoWeight5', 'value'), Output('CommoWeight6', 'value')],
    [Input('MoreCommos', 'n_clicks'), Input('LessCommos', 'n_clicks')])
def update_text(Plus, Moins):
    Val = Plus - Moins
    Left, Right = {'display' : 'inline-flex', 'position': 'relative'}, {'display' : 'inline-flex', 'position': 'relative',  'margin-left': '100px',}
    if Val <0: Val = 0
    if Val < 1: return {'display': 'none'} , {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'},0,0,0,0,0
    if Val < 2: return Right, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'},  dash.no_update,0,0,0,0
    if Val < 3: return Right, Left, {'display': 'none'}, {'display': 'none'}, {'display': 'none'},  dash.no_update,dash.no_update,0,0,0
    if Val < 4: return Right, Left, Right, {'display': 'none'}, {'display': 'none'} ,  dash.no_update,dash.no_update,dash.no_update,0,0
    if Val < 5: return Right, Left, Right, Left, {'display': 'none'},  dash.no_update,dash.no_update,dash.no_update,dash.no_update,0
    else:
        return Right, Left, Right, Left, Right, dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update
    
    


@app.callback(
    Output("ReturnsGraph", "figure"),
    [Input("CommoWeight1", "value"), Input("CommoPick1", "value"), Input("MaturityPick1", "value"), Input("CommoWeight2", "value"), Input("CommoPick2", "value"), Input("MaturityPick2", "value"),
     Input("CommoWeight3", "value"), Input("CommoPick3", "value"), Input("MaturityPick3", "value"), Input("CommoWeight4", "value"), Input("CommoPick4", "value"), Input("MaturityPick4", "value"),
     Input("CommoWeight5", "value"), Input("CommoPick5", "value"), Input("MaturityPick5", "value"), Input("CommoWeight6", "value"), Input("CommoPick6", "value"), Input("MaturityPick6", "value"),
     Input("ReturnsGraph", "relayoutData")
     ])
def update_graph2(Weight1, Commo1, Maturity1, Weight2, Commo2, Maturity2, Weight3, Commo3, Maturity3, Weight4, Commo4, Maturity4, Weight5, Commo5, Maturity5, Weight6, Commo6, Maturity6, Date):
    if Weight1 is None: Weight1 = 0
    if Weight2 is None: Weight2 = 0
    if Weight3 is None: Weight3 = 0
    if Weight4 is None: Weight4 = 0
    if Weight5 is None: Weight5 = 0
    if Weight6 is None: Weight6 = 0
        
    df = Weight1*Ret[Commo1+Maturity1] + Weight2*Ret[Commo2+Maturity2] + Weight3*Ret[Commo3+Maturity3] + Weight4*Ret[Commo4+Maturity4] + Weight5*Ret[Commo5+Maturity5] + Weight6*Ret[Commo6+Maturity6]
    df1 = df+1
    if Date is not None: 
        if 'xaxis.range[0]' in Date.keys(): 
            df1 = df1[df1.index >= int(Date['xaxis.range[0]'].split(" ")[0].replace("-",""))]
    df1 = df1.dropna()
    df1.iloc[0] = 100   
  
    return {
        'data': [    dict(x= pd.to_datetime(df1.index, format="%Y%m%d") , 
                          y= [x for x in df1.cumprod()], 
                          name= 'Cumulated Returns')
                 ],
        'layout': dict(title='Returns')
        }

@app.callback(
    Output("ACF", "figure"),
    [Input("CommoWeight1", "value"), Input("CommoPick1", "value"), Input("MaturityPick1", "value"), Input("CommoWeight2", "value"), Input("CommoPick2", "value"), Input("MaturityPick2", "value"), Input("ReturnsGraph", "relayoutData"),])
def update_graph3(Weight1, Commo1, Maturity1, Weight2, Commo2, Maturity2, Date):
    Title = ""
    if Weight1 is None:
        Weight1 = 0
    if Weight2 is None:
        Weight2 = 0
    if Weight1 != 0: Title = Title + Commo1
    if Weight2 != 0: Title = Title + Commo2
    if len(Title) > 2: Title = Title[:2] +" & " + Title[2:]
    df = Weight1 * Ret[Commo1+Maturity1] + Weight2 * Ret[Commo2+Maturity2]
    if Date is not None: 
        if 'xaxis.range[0]' in Date.keys(): 
            df = df[(df.index >= int(Date['xaxis.range[0]'].split(" ")[0].replace("-",""))) & (df.index <= int(Date['xaxis.range[1]'].split(" ")[0].replace("-","")))]

    
    
    ACFListe = []
    ConfLvl = []
    for x in range(1,40):
        ACFListe.append( pd.concat((df, df.shift(x)), axis=1).dropna().corr().iloc[0,1] )
        ConfLvl.append( 1.96 / np.sqrt(len(df)-x) )
    return {
        'data': [    dict(x= [x for x in range(1,len(ACFListe))] , 
                          y= [x for x in ACFListe], 
                          type= 'bar',
                          name= 'Cumulated Returns'),
                     dict(x= [x for x in range(1,len(ACFListe))] , 
                          y= [x for x in ConfLvl], 
                          color = 'black',
                          mode= 'line',
                          line=dict(color='black', dash='dash'),
                          name= 'Confidence Level'),
                       dict(x= [x for x in range(1,len(ACFListe))] , 
                            y= [-x for x in ConfLvl], 
                            color = 'black',
                            showlegend =False,
                            mode= 'line',
                            line=dict(color='black', dash='dash'),),
                     
                 
                 ],
        'layout': dict(title='AutoCorrelation Function',
                       xaxis={'tickmode':'linear'},)
        }

 
@app.callback(
    [Output('Correltable', 'data'), Output('Correltable', 'columns')],
    [Input('FutureMaturity', "value")])
def update_table(value):
    Correl = round(Ret[[x for x in Ret.columns if str(value) in x]][-252*3:].corr(), 2).reset_index()
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