
from graphs.abstract import InteractiveGraph
from graphs.utils import df_to_plotly_xyz

import numpy as np
import pandas as pd

import plotly.figure_factory as ff
import plotly.graph_objects as go


class ParamHeatmapGraph(InteractiveGraph):
    def __init__(self, metrics, params):
        super().__init__(name="param-heatmap-graph")
        self.metrics = metrics
        self.params = params

        self.register_dropdown("Hyperparameter", "param1",
                               self.params, width="80%")
        self.register_dropdown("Hyperparameter", "param2",
                               self.params, width="80%", default_index=1)
        self.register_dropdown("Metric", "metric", self.metrics, width="80%")

    @staticmethod
    def update_fn(df_as_json, param1, param2, metric):
        dff = pd.read_json(df_as_json, orient='split')
        reduced_df = dff[[param1, param2, metric]]
        grouped_df = reduced_df.groupby(
            [param1, param2], as_index=False).mean()
        pivoted_df = grouped_df.pivot(
            index=param2, columns=param1, values=metric)

        x, y, z = df_to_plotly_xyz(pivoted_df)
        z_text = np.around(z, decimals=2)
        x = [str(s) for s in x]
        y = [str(s) for s in y]

        layout_heatmap = go.Layout(
            title=f'Heatmap of {metric}',
            xaxis=dict(title=param1),
            yaxis=dict(title=param2))

        heatmap = go.Heatmap(z=z, x=x, y=y,
                             colorscale='bluered',
                             showscale=True)
        fig = go.Figure(heatmap)
        fig.layout = layout_heatmap
        fig_annot = ff.create_annotated_heatmap(z, annotation_text=z_text
                                                )
        fig.layout.annotations = fig_annot.layout.annotations
        return fig
