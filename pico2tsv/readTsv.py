from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np 
app = Dash(__name__)

app.layout = html.Div([
    html.H4('PicoAdc24 data'),
    dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0),
    dcc.Graph(id="graphA"),
    dcc.Graph(id="graphB"),
])

@app.callback(
    Output('graphA', 'figure'),
    [Input('interval-component', "n_intervals")]
)
def display_graph(n_clicks):
    df = pd.read_csv('./pico2tsv/example.csv') # replace with your own data source
    pico24 = []
    for i in range(1,len(df['channel1']),1):
        #=SQRT(B - SQRT(A))/1000
        pico24.append(df.iat[i,1])
        # pico24.append(np.sqrt(np.sqrt(df.iat[i,1]) - np.sqrt(df.iat[i,0]))/1000)
    newDf = pd.DataFrame(pico24)
    # print(newDf)
    fig = px.line(newDf)
    return fig
@app.callback(
    Output('graphB', 'figure'),
    [Input('interval-component', "n_intervals")]
)
def display_graph(n_clicks):
    df = pd.read_csv('./pico2tsv/example.csv') # replace with your own data source
    pico24 = []
    for i in range(1,len(df['channel1']),1):
        #=SQRT(B - SQRT(A))/1000
        pico24.append(df.iat[i,2])
        # pico24.append(np.sqrt(np.sqrt(df.iat[i,1]) - np.sqrt(df.iat[i,0]))/1000)
    newDf = pd.DataFrame(pico24)
    # print(newDf)
    fig = px.line(newDf)
    return fig

app.run_server(debug=True)