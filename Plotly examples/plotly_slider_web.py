from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash
import dash_cytoscape as cyto
import dash_html_components as html
import math as m

app = Dash(__name__)
app.layout = html.Div([
    html.H3('point interactive'),
    dcc.Graph(id="scatter-plot"),
    html.P("Filter by petal width:"),
    dcc.Slider(
        id='x-slider',
        step=0.2,
        min=1,
        max=10
    ),
    dcc.Slider(
        id='y-slider',
        step=0.2,
        min=1,
        max=10
    )
])


def distance(x1, x2, y1, y2):
    measurment = m.floor(m.sqrt(x1-x2) + m.sqrt(y1-y2))
    return measurment

app = dash.Dash(__name__)
pt1x= 75
app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-two-nodes',
        
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '800px'},
        elements=[
            {'data': {'id': 'one', 'label': 'Node 1'}, 'position': {'x': pt1x, 'y': 75}},
            {'data': {'id': 'two', 'label': 'Node 2'}, 'position': {'x': 200, 'y': 200}},
            {'data': {'source': 'one', 'target': 'two'}}
        ]
    ),
    html.P(pt1x),
    dcc.Slider(
        id='x-slider',
        step=0.2,
        min=1,
        max=10
    ),
    dcc.Slider(
        id='y-slider',
        step=0.2,
        min=1,
        max=10
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
