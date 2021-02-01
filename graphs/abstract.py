from abc import ABC
from graphs.utils import connect_columns, label
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output


class InteractiveGraph(ABC):
    def __init__(self, name):
        self.name = name
        self.graph_div = html.Div([dcc.Graph(id=name)])
        self.control_divs = []
        self.input_ids = []
        self.input_names = []
        self._final_div = None

    @property
    def final_div(self):
        if not self._final_div:
            self._final_div = html.Div(
                [self.graph_div, connect_columns(*self.control_divs)])
        return self._final_div

    def register_with_app(self, app, data_input):
        output = Output(self.name, "figure")

        data_input = Input(*data_input)
        control_inputs = [Input(input_id, "value")
                          for input_id in self.input_ids]
        app.callback(output, data_input, *control_inputs)(self.update_fn)

    def register_dropdown(self, title, name, options, width="80%", default_index=0):
        div_id = self.name + '-' + name
        div = html.Div([label(title), dcc.Dropdown(
            id=div_id,
            options=[{'label': it, 'value': it} for it in options],
            value=options[default_index]
        )], style={"width": width})

        self.control_divs.append(div)
        self.input_ids.append(div_id)
        self.input_names.append(name)
