from dash import html, dcc, dash_table
import plotly.graph_objs as go
from data_handler import get_processed_data

# Fetch and process the data
data_url = 'https://github.com/vaastav/Fantasy-Premier-League/blob/master/data/2023-24/gws/merged_gw.csv?raw=true'
df = get_processed_data(data_url)

unique_players = sorted(df['name'].unique())
selected_columns = [
    'xP', 'assists', 'bonus', 'bps', 'clean_sheets', 'creativity',
    'goals_conceded', 'goals_scored', 'ict_index', 'influence', 'minutes',
    'saves', 'selected', 'threat', 'total_points', 'transfers_balance',
    'value', 'yellow_cards', 'red_cards'
]

def graphs_tab():
    return html.Div([
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

def overview_tab():
    return html.Div([
        html.Div([
            dcc.Input(id='overview-weeks-input', type='number', placeholder='Number of Weeks', value=4),
            html.Button('Update', id='overview-update-button'),
        ], style={'margin-bottom': '20px'}),

        html.Div([
            html.Div([
            html.Label("Best Performers by Points (GK)", style={'font-weight': 'bold'}),
            dash_table.DataTable(
            id='table-gk-points',
            columns=[{'name': col, 'id': col} for col in ['name', 'total_points', 'value']],
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'left', 'fontSize': '10px'},
            style_header={'backgroundColor': 'white', 'fontWeight': 'bold'}
        )], className='table-container'),
        html.Div([
        html.Label("Best Performers by Points (DEF)", style={'font-weight': 'bold'}),
            dash_table.DataTable(
            id='table-def-points',
            columns=[{'name': col, 'id': col} for col in ['name', 'total_points', 'value']],
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'left', 'fontSize': '10px'},
            style_header={'backgroundColor': 'white', 'fontWeight': 'bold'}
        )], className='table-container'),
        html.Div([
        html.Label("Best Performers by Points (MID)", style={'font-weight': 'bold'}),
            dash_table.DataTable(
            id='table-mid-points',
            columns=[{'name': col, 'id': col} for col in ['name', 'total_points', 'value']],
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'left', 'fontSize': '10px'},
            style_header={'backgroundColor': 'white', 'fontWeight': 'bold'}
        )], className='table-container'),
        html.Div([
        html.Label("Best Performers by Points (FWD)", style={'font-weight': 'bold'}),
            dash_table.DataTable(
            id='table-fwd-points',
            columns=[{'name': col, 'id': col} for col in ['name', 'total_points', 'value']],
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'left', 'fontSize': '10px'},
            style_header={'backgroundColor': 'white', 'fontWeight': 'bold'}
        )], className='table-container'),
        html.Div([
        html.Label("Best Performers by Point Value (GK)", style={'font-weight': 'bold'}),
            dash_table.DataTable(
            id='table-gk-value',
            columns=[{'name': col, 'id': col} for col in ['name', 'total_points', 'value']],
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'left', 'fontSize': '10px'},
            style_header={'backgroundColor': 'white', 'fontWeight': 'bold'}
        )], className='table-container'),
        html.Div([
        html.Label("Best Performers by Point Value (DEF)", style={'font-weight': 'bold'}),
            dash_table.DataTable(
            id='table-def-value',
            columns=[{'name': col, 'id': col} for col in ['name', 'total_points', 'value']],
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'left', 'fontSize': '10px'},
            style_header={'backgroundColor': 'white', 'fontWeight': 'bold'}
        )], className='table-container'),
        html.Div([
        html.Label("Best Performers by Point Value (MID)", style={'font-weight': 'bold'}),
            dash_table.DataTable(
            id='table-mid-value',
            columns=[{'name': col, 'id': col} for col in ['name', 'total_points', 'value']],
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'left', 'fontSize': '10px'},
            style_header={'backgroundColor': 'white', 'fontWeight': 'bold'}
        )], className='table-container'),
        html.Div([
        html.Label("Best Performers by Point Value (FWD)", style={'font-weight': 'bold'}),
            dash_table.DataTable(
            id='table-fwd-value',
            columns=[{'name': col, 'id': col} for col in ['name', 'total_points', 'value']],
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'left', 'fontSize': '10px'},
            style_header={'backgroundColor': 'white', 'fontWeight': 'bold'}
        )], className='table-container'),
        ], style={'display': 'grid', 'grid-template-columns': 'repeat(auto-fill, minmax(300px, 1fr))', 'grid-gap': '5px'}),
    ])


def tables_tab():
    return html.Div([
        html.Label("Select Statistic:"),
        dcc.Dropdown(
            id='column-select',
            options=[{'label': stat, 'value': stat} for stat in df.columns],
            value=['name', 'team', 'value', 'total_points'],  # default value
            multi=True
        ),
        html.Div(id='aggregation-selectors'), # Placeholder for aggregation selectors
        html.Div([
            html.Label("Filter by Value:"),
            dcc.RangeSlider(
                id='value-range-slider',
                min=df['value'].min(),
                max=df['value'].max(),
                value=[df['value'].min(), df['value'].max()],
                marks={i: str(i) for i in [int(df['value'].min()), int(df['value'].max())]}
            )
        ]),
        html.Div([
            html.Label("Filter by GW:"),
            dcc.RangeSlider(
                id='GW-range-slider',
                min=df['GW'].min(),
                max=df['GW'].max(),
                value=[df['GW'].min(), df['GW'].max()],
                marks={i: str(i) for i in [int(df['GW'].min()), int(df['GW'].max())]}
            )
        ]),
        html.Div([
            html.Label("Filter by Position:"),
            dcc.Checklist(
                id='position-filter',
                options=[
                    {'label': 'GK', 'value': 'GK'},
                    {'label': 'DEF', 'value': 'DEF'},
                    {'label': 'MID', 'value': 'MID'},
                    {'label': 'FWD', 'value': 'FWD'}
                ],
                value=['GK'],  # Default selected values
                inline=True
            )
        ]),
        html.Div([
            html.Label("Sort by:"),
            dcc.Dropdown(
                id='sort-by-select',
                options=[{'label': col, 'value': col} for col in df.columns],
                value='total_points',  # Default sort column
                multi=False
            ),
            dcc.RadioItems(
                id='sort-order',
                options=[{'label': 'Ascending', 'value': 'asc'}, {'label': 'Descending', 'value': 'desc'}],
                value='desc',
                inline=True
            )
        ]),
        dash_table.DataTable(id='configurable-table')
    ])