import dash_html_components as html


def df_to_plotly_xyz(df):
    x = df.columns.tolist()
    y = df.index.tolist()
    z = df.values.tolist()
    return x, y, z


def label(name):
    return html.Label([name],
                      style={'font-weight': 'bold', "text-align": "center"})


def connect_columns(*columns, total_width=1.0):
    width = int(100 * total_width) // len(columns)
    cols = [html.Div([col],
                     style={'display': 'inline-block', "width": f"{width}%"})
            for col in columns]
    col_divs = html.Div(cols, className="row")
    return col_divs


def graph_with_dropdowns(graph, *controls):
    return html.Div([graph, connect_columns(*controls)])
