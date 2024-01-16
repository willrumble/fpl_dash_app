from dash.dependencies import Input, Output, State
from app import app
from layouts import graphs_tab, tables_tab, overview_tab, df  # Import the DataFrame
import plotly.graph_objs as go
from dash import html, dcc
from dash.exceptions import PreventUpdate
import pandas as pd

@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value')]
)
def render_content(tab):
    if tab == 'tab-graphs':
        return graphs_tab()  # Use the function from layouts.py
    elif tab == 'tab-tables':
        return tables_tab()
    elif tab == 'tab-overview':
        return overview_tab()


@app.callback(
    Output('trailing-period-input', 'style'),
    [Input('toggle-trailing', 'value')]
)
def toggle_input_box(toggle_value):
    if 'ON' in toggle_value:
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
    Output('graphs-container', 'children'),
    [
        Input('player-dropdown', 'value'),
        Input('stat-dropdown', 'value'),
        Input('trailing-lookback', 'value'),
        Input('toggle-trailing', 'value'),
        Input('num-cols-input', 'value')
    ]
)
def update_graphs(selected_players, selected_stats, lookback, toggle_value, num_cols):
    # Ensure selected_stats is a list even if it's a single selection
    if not isinstance(selected_stats, list):
        selected_stats = [selected_stats]
    
    if not selected_players or not selected_stats:
        return html.Div([
            dcc.Graph(
                figure={
                    'data': [],
                    'layout': {
                        'title': 'No Data to Display',
                        'xaxis': {'title': 'Game Week'},
                        'yaxis': {'title': 'Statistic'}
                    }
                }
            )
        ])

    # Determine the number of rows and columns for the grid layout
    num_stats = len(selected_stats)

    if not num_cols or num_cols < 1:
        num_cols = 2

    num_rows = (num_stats + 1) // num_cols

    # Create a list to store the graph components
    graphs = []

    for stat in selected_stats:
        fig = go.Figure()

        for player in selected_players:
            filtered_df = df[df['name'] == player]

            # Apply trailing average if enabled and a valid lookback is provided
            if 'ON' in toggle_value and lookback is not None and lookback > 0:
                filtered_df[stat] = filtered_df[stat].rolling(window=lookback, min_periods=1).mean()
                title = f'Trailing Avg ({lookback} GW) of {stat}'
            else:
                title = f'{stat}'

            fig.add_trace(go.Scatter(
                x=filtered_df['GW'], 
                y=filtered_df[stat],
                mode='lines+markers',
                name=player
            ))

        # Update layout of the figure
        fig.update_layout(
            title=title,
            xaxis_title='Game Week',
            yaxis_title=stat,
            legend_title="Players"
        )

        # Append the figure wrapped in an HTML Div to the list of graphs
        graphs.append(html.Div(dcc.Graph(figure=fig), className='grid-item'))

    # Determine the grid layout style
    grid_style = {
        'display': 'grid',
        'gridTemplateColumns': f'repeat({num_cols}, 1fr)',
        'gridGap': '10px'
    }

    return html.Div(graphs, style=grid_style)

@app.callback(
Output('configurable-table', 'columns'),
[Input('column-select', 'value')]
)
def update_table_columns(selected_columns):
    if not isinstance(selected_columns, list):
        selected_columns = [selected_columns]
    columns = [{'name': col, 'id': col} for col in selected_columns]
    return columns

@app.callback(
    Output('configurable-table', 'data'),
    [Input('column-select', 'value'),
     Input('value-range-slider', 'value'),
     Input('GW-range-slider', 'value'),
     Input('position-filter', 'value'),
     Input('sort-by-select', 'value'),
     Input('sort-order', 'value')]
)
def update_table(selected_columns, value_range, GW_range, selected_positions, sort_by, sort_order):
    # Check if any essential input is missing
    if not selected_columns or not sort_by:
        raise PreventUpdate

    # Filter the DataFrame based on the value range and position
    filtered_df = df[df['value'].between(value_range[0], value_range[1])]
    filtered_df = filtered_df[filtered_df['GW'].between(GW_range[0], GW_range[1])]
    if selected_positions:
        filtered_df = filtered_df[filtered_df['position'].isin(selected_positions)]

    # Sort the DataFrame by Game Week (GW) first to get the most recent values
    filtered_df = filtered_df.sort_values(by='GW', ascending=False)

    # Columns to take the most recent value
    recent_value_cols = ['name', 'team', 'value']
    recent_values = filtered_df.groupby('name')[recent_value_cols].first()

    # Other columns to sum
    sum_columns = [col for col in selected_columns if col not in recent_value_cols]
    summed_values = filtered_df.groupby('name')[sum_columns].sum()

    # Combine the two DataFrames
    final_df = pd.concat([recent_values, summed_values], axis=1)

    # Sort the final DataFrame as per user's choice
    final_df = final_df.sort_values(by=sort_by, ascending=(sort_order == 'asc'))

    # Ensure only selected columns are included in the final DataFrame
    final_df = final_df[selected_columns]

    data = final_df.to_dict('records')
    return data

