from dash import html, dcc
from app import app
import callbacks
import layouts

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Overview', value='tab-overview'),
        dcc.Tab(label='Graphs', value='tab-graphs'),
        dcc.Tab(label='Tables', value='tab-tables'),
    ], id='tabs', value='tab-graphs'),
    html.Div(id='tabs-content')
])

if __name__ == '__main__':
    app.run_server(debug=True)
