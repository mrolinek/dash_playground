import dash_table
import dash_html_components as html
from dash.dependencies import Input, Output

from data_table.utils import table_type, split_filter_part, tooltip_friendly


class InteractiveTable(object):
    def __init__(self, init_df):
        self.init_df = init_df
        self.div = html.Div([
            dash_table.DataTable(
                id='data_table',
                columns=[{"name": i,
                          "id": i,
                          'type': table_type(self.init_df[i]),
                          "hideable": "last",
                          }
                         for i in self.init_df.columns],

                filter_action="custom",
                sort_action="custom",
                sort_mode="multi",
                page_action="custom",
                page_current=0,
                page_size=15,
                sort_by=[],
                style_table={'overflowX': 'scroll'},
                style_header={'whiteSpace': 'normal',
                              'height': 'auto'},
                style_data={
                    'minWidth': '100px',
                    'maxWidth': '200px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis'
                }), html.Div(id='full_data', style={'display': 'none'})], className='row')

        self.displayed_data_id = ('data_table', 'data')
        self.full_data_id = ('full_data', 'children')
        self.tooltip_data_id = ('data_table', 'tooltip_data')

    @staticmethod
    def update_fn(page_current, page_size, sort_by, filter_str, *, init_df):
        filter_str = filter_str or ''
        sort_by = sort_by or []
        filtering_expressions = filter_str.split(' && ')
        dff = init_df.copy()
        for filter_part in filtering_expressions:
            col_name, operator, filter_value = split_filter_part(filter_part)

            if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
                # these operators match pandas series operator method names
                dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
            elif operator == 'contains':
                dff = dff.loc[dff[col_name].str.contains(filter_value)]
            elif operator == 'datestartswith':
                # this is a simplification of the front-end filtering logic,
                # only works with complete fields in standard format
                dff = dff.loc[dff[col_name].str.startswith(filter_value)]

        if sort_by:
            dff = dff.sort_values(
                [col['column_id'] for col in sort_by],
                ascending=[
                    col['direction'] == 'asc'
                    for col in sort_by
                ],
                inplace=False
            )

        tooltip_data = [{column: {'value': tooltip_friendly(str(value)), 'type': 'markdown'}
                         for column, value in row.items()
                         } for row in dff.to_dict('records')]

        this_page = dff.iloc[page_current *
                             page_size: (page_current + 1) * page_size].to_dict('records')

        all_data = dff.to_json(date_format='iso', orient='split')
        # JSON serialization because fo dates

        return this_page, all_data, tooltip_data

    def register_with_app(self, app):
        def callback_fn(*args, **kwargs):
            return InteractiveTable.update_fn(*args, init_df=self.init_df, **kwargs)

        outputs = [Output(*self.displayed_data_id),
                   Output(*self.full_data_id),
                   Output(*self.tooltip_data_id)]

        inputs = [Input('data_table', "page_current"),
                  Input('data_table', "page_size"),
                  Input('data_table', "sort_by"),
                  Input('data_table', "filter_query")]

        app.callback(outputs, inputs)(callback_fn)
