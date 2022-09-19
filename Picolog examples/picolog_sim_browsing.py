from re import template
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from jupyter_dash import JupyterDash
from dash import Input, Output, html, dcc

import time
from datalog.adc.adc import Adc
from datalog.adc.config import AdcConfig
from datalog.data import DataStore

# picolog setting
adc24 = AdcConfig()
adc = Adc.load_from_config(adc24)
datastore = DataStore(1000)
print(adc.get_full_unit_info())
adc.open()
    
# code and plot setup
# settings
pd.options.plotting.backend = "plotly"
countdown = 20
#global df
arr = np.array(np.mat([0,0]))
# sample dataframe of a wide format
# np.random.seed(4)
cols = ['pico1', 'picoA']
X = np.random.randn(2,len(cols))  
df=pd.DataFrame(X, columns=cols)
df.iloc[0]=0


# plotly figure
fig = df.plot.line(template = 'simple_white')

app = JupyterDash(__name__)
app.layout = html.Div([
    html.H1("Streaming of Picolog data"),
            dcc.Interval(
            id='interval-component',
            interval=5*1000, # in milliseconds
            n_intervals=0
        ),
    dcc.Graph(id='graph'),
])

@app.callback(
    Output('graph', 'figure'),
    [Input('interval-component', "n_intervals")]
)

def streamFig(value):  
    global df
    global arr, adc, datastore
    
    # open ADC
    i = 0
    with adc.get_retriever(datastore) as retriever:
        # default last reading time
        last_reading = 0

        while(retriever.retrieving):
            # look for new readings
            new_readings = datastore.get_readings(pivot_time=last_reading)
            if len(new_readings):
                readingData = str(new_readings[-1])
                # print(readingData)
                arr = np.array(np.mat(readingData.split(','),dtype=float))
                i += 1
                # arr = np.array(np.mat(readingData.split(',')))
                # Define callback to update graph
            # sleep for 1 second
            time.sleep(0.5)
            if(i == 20):
                break
    
    # Y = np.array(np.mat(np.random.randint(0,10)),len(cols)) 
    # Y = np.random.randn(2,len(cols))
    # v = np.sqrt(arr.item(1) - np.sqrt(arr.item(0)))/1000
    # print(v)
    df2 = pd.DataFrame(arr, columns = cols)
    
    # df = df.append(df2, ignore_index=True)#.reset_index()
    df = pd.concat([df, df2], ignore_index=True)
    print(df)
    df.tail()
    df3=df.copy()
    # df3 = df3.cumsum()
    # fig = df.plot(template = 'simple_white')
    fig = df.plot(template = 'simple_white')
    #fig.show()
    colors = px.colors.qualitative.Plotly
    # colors = ['#009999', '#00b359', '#ff3333', '#db4dff', '#cc6699']
    for i, col in enumerate(df3.columns):
            fig.add_annotation(x=df3.index[-1], y=df3[col].iloc[-1],
                                text = str(df3[col].iloc[-1])[:4],
                                align="right",
                                arrowcolor = 'rgba(0,0,0,0)',
                                ax=25,
                                ay=0,
                                yanchor = 'middle',
                                font = dict(color = colors[i]))
    
    return(fig)

if __name__== '__main__':
    app.run_server(mode='external', port = 8069, dev_tools_ui=True, #debug=True,
            dev_tools_hot_reload =True, threaded=True)
