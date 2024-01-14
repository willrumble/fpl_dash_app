# Import necessary libraries
import dash
from dash import html, dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from data_handler import fetch_data, process_data

# URL of the raw data file in the GitHub repository
data_url = 'https://github.com/vaastav/Fantasy-Premier-League/blob/master/data/2023-24/gws/merged_gw.csv?raw=true'

# Fetch and process the data
raw_data = fetch_data(data_url)
df = process_data(raw_data)

unique_players = df['name'].unique()
selected_columns = ['minutes', 'xP', 'goals_scored']


# Use processed_data in your Dash components/callbacks


# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("FPL Player Statistics"),

    html.Label("Select Player:"),
    dcc.Dropdown(
        id='player-dropdown',
        options=[{'label': player, 'value': player} for player in unique_players],
        value=unique_players[0]  # default value
    ),

    html.Label("Select Statistic:"),
    dcc.Dropdown(
        id='stat-dropdown',
        options=[{'label': stat, 'value': stat} for stat in selected_columns],
        value=selected_columns[0]  # default value
    ),

    dcc.Graph(id='performance-graph')
])


@app.callback(
Output('performance-graph', 'figure'),
[Input('player-dropdown', 'value'),
Input('stat-dropdown', 'value')]
)
def update_graph(selected_player, selected_stat):
    # Filter the DataFrame based on the selected player
    filtered_df = df[df['name'] == selected_player]

    # Create the figure
    fig = go.Figure(data=[
        go.Scatter(
            x=filtered_df['GW'], 
            y=filtered_df[selected_stat],
            mode='lines+markers'
        )
    ])

    # Update layout of the figure
    fig.update_layout(
        title=f'{selected_stat} over Game Weeks for {selected_player}',
        xaxis_title='Game Week',
        yaxis_title=selected_stat
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

