# Import necessary libraries
import dash
from dash import dcc, html, Input, Output
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from data_handler import fetch_data, process_data

# URL of the raw data file in the GitHub repository
data_url = 'https://github.com/vaastav/Fantasy-Premier-League/blob/master/data/2023-24/gws/merged_gw.csv?raw=true'

# Fetch and process the data
raw_data = fetch_data(data_url)
df = process_data(raw_data)

unique_players = sorted(df['name'].unique())
selected_columns = [
    'xP', 'assists', 'bonus', 'bps', 'clean_sheets', 'creativity',
    'goals_conceded', 'goals_scored', 'ict_index', 'influence', 'minutes',
    'saves', 'selected', 'threat', 'total_points', 'transfers_balance',
    'value', 'yellow_cards', 'red_cards'
]



# Use processed_data in your Dash components/callbacks


# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("FPL Player Statistics"),
    html.Div([
        html.Label('Enable Trailing Average:', style={'margin-right': '10px'}),
        dcc.Checklist(
            id='toggle-trailing',
            options=[{'label': '', 'value': 'ON'}],
            value=[],
            inputStyle={"margin-right": "5px"}
        )
    ], style={'display': 'flex', 'align-items': 'center'}),
    html.Div(id='trailing-period-input', style={'display': 'none'}, children=[
        dcc.Input(
            id='trailing-lookback', 
            type='number', 
            placeholder='Enter lookback period'
        )
    ]),
    html.Div([
        html.Label('Number of Columns:'),
        dcc.Input(
            id='num-cols-input',
            type='number',
            value=2,  # default value
            min=1,    # minimum value
            style={'width': '100px', 'margin-left': '5px'}
        )
    ], style={'margin-bottom': '10px'}),

    html.Label("Select Player:"),
    dcc.Dropdown(
        id='player-dropdown',
        options=[{'label': player, 'value': player} for player in unique_players],
        value='Erling Haaland',  # default value
        multi=True
    ),

    html.Label("Select Statistic:"),
    dcc.Dropdown(
        id='stat-dropdown',
        options=[{'label': stat, 'value': stat} for stat in selected_columns],
        value=selected_columns[0],  # default value
        multi=True
    ),

    html.Div(id='graphs-container')
])

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



if __name__ == '__main__':
    app.run_server(debug=True)

