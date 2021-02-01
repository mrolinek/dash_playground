from data_table.data_table import InteractiveTable
import os
import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

from graphs.utils import connect_columns
from graphs import ParamDensitiesGraph, ParamHeatmapGraph, MetricCorrelationGraph


df = pd.read_csv("results_raw.csv")
metrics = [col for col in df.columns if "score" in col]
params = [col for col in df.columns if "player_params" in col]

app = dash.Dash(__name__)

interactive_table = InteractiveTable(init_df=df)

interactive_graphs = [ParamDensitiesGraph(params=params, metrics=metrics),
                      ParamHeatmapGraph(params=params, metrics=metrics),
                      MetricCorrelationGraph(metrics=metrics)]

interactive_table.register_with_app(app)

for graph in interactive_graphs:
    graph.register_with_app(app, data_input=interactive_table.full_data_id)

graphs_div = connect_columns(*[graph.final_div for graph in interactive_graphs])

app.layout = html.Div([
    html.H1("Data summary"),
    graphs_div,
    dcc.Input(style={"margin-top": "50px"}),
    interactive_table.div])

app.run_server(debug=True, port=os.getenv('PORT', 6431))
