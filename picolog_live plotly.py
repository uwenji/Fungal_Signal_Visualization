import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
#picolog
import time
from datalog.adc.adc import Adc
from datalog.adc.config import AdcConfig
from datalog.data import DataStore


#picolog setup
# load ADC with default config
adc = Adc.load_from_config(AdcConfig())
if adc.is_open:
    adc.open()
adc._get_hrdl_lib()
# datastore holding last 1000 readings
datastore = DataStore(1000)

adc.configure()
print(adc.get_full_unit_info())



# code and plot setup
# settings
pd.options.plotting.backend = "plotly"
countdown = 20
#global df

# sample dataframe of a wide format
np.random.seed(4); cols = list('abcde')
X = np.random.randn(50,len(cols))  
df=pd.DataFrame(X, columns=cols)
df.iloc[0]=0;

# plotly figure
fig = df.plot(template = 'simple_white')

app = JupyterDash(__name__)
app.layout = html.Div([
    html.H1("Streaming of Picolog data"),
            dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        ),
    dcc.Graph(id='graph'),
])

# Define callback to update graph
@app.callback(
    Output('graph', 'figure'),
    [Input('interval-component', "n_intervals")]
)


    
    with adc.get_retriever(datastore) as retriever:
        # default last reading time
        last_reading = 0
        
        while(True):
            # look for new readings
            new_readings = datastore.get_readings(pivot_time=last_reading)
            
            Y = np.ndarray(1,len(cols))  
            if len(new_readings):
                for i in len(new_readings):
                    Y.put(i, new_readings[i])
        df2 = pd.DataFrame(Y, columns = cols)
        df = df.append(df2, ignore_index=True)#.reset_index()
        df.tail()
        df3=df.copy()
        df3 = df3.cumsum()
        fig = df3.plot(template = 'simple_white')
        #fig.show()
        return(fig)

app.run_server(mode='external', port = 8069, dev_tools_ui=True, #debug=True,
              dev_tools_hot_reload =True, threaded=True)

