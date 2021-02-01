
from graphs.abstract import InteractiveGraph
from graphs.utils import df_to_plotly_xyz

import numpy as np
import pandas as pd

import plotly.figure_factory as ff
import plotly.graph_objects as go

from functools import partial


class MetricCorrelationGraph(InteractiveGraph):
    def __init__(self, metrics):
        super().__init__(name="metric-correlation-graph")
        self.metrics = metrics

        corr_options = ['Spearman', 'Pearson', 'Kendall']

        self.register_dropdown(
            "Correlation type", "correlation_type", corr_options)

        self.update_fn = partial(
            MetricCorrelationGraph.update_fn_full, metrics=self.metrics)

    @staticmethod
    def update_fn_full(df_as_json, correlation_type, *, metrics):
        dff = pd.read_json(df_as_json, orient='split')
        reduced_df = dff[metrics]
        corr = reduced_df.corr(correlation_type.lower())

        x, y, z = df_to_plotly_xyz(corr)
        z_text = np.around(z, decimals=2)
        x = [str(s) for s in x]
        y = [str(s) for s in y]

        layout_heatmap = go.Layout(title='Metric Correlation Plot')

        heatmap = go.Heatmap(z=z, x=x, y=y,
                             colorscale=["red", "green"],
                             showscale=True)
        fig = go.Figure(heatmap)
        fig.layout = layout_heatmap
        fig_annot = ff.create_annotated_heatmap(z, annotation_text=z_text
                                                )
        fig.layout.annotations = fig_annot.layout.annotations
        return fig
