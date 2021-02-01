
from graphs.abstract import InteractiveGraph

import pandas as pd

import plotly.figure_factory as ff
import plotly.express as px


class ParamDensitiesGraph(InteractiveGraph):
    def __init__(self, metrics, params):
        super().__init__(name="param-density-graph")
        self.metrics = metrics
        self.params = params

        self.register_dropdown("Hyperparameter", "param",
                               self.params, width="80%")
        self.register_dropdown("Metric", "metric", self.metrics, width="80%")

    @staticmethod
    def update_fn(df_as_json, param, metric):
        df = pd.read_json(df_as_json, orient='split')
        values = df[param].unique()

        data = [list(df.loc[df[param] == it][metric]) for it in values]
        fig = ff.create_distplot(data, [str(i) for i in values], show_hist=False,
                                 colors=px.colors.sequential.Plasma_r)

        fig.update_layout(title=f'Densities of {metric} by {param}')
        return fig
