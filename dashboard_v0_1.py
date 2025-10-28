import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd

LOG_FILE = "network_traffic.log"

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(style={'backgroundColor': '#111111', 'color': '#FFFFFF'}, children=[
    html.H1("Home Network Monitor - v0.1", style={'textAlign': 'center'}),
    
    # This component will trigger our callback every 3 seconds
    dcc.Interval(
        id='interval-component',
        interval=3*1000,  # in milliseconds (3 seconds)
        n_intervals=0
    ),
    
    # This table will display our live data
    dash_table.DataTable(
        id='live-traffic-table',
        columns=[
            {"name": "Timestamp", "id": "timestamp"},
            {"name": "Protocol", "id": "protocol"},
            {"name": "Source IP", "id": "src_ip"},
            {"name": "Destination IP", "id": "dst_ip"},
            {"name": "Dest Port", "id": "dst_port"},
        ],
        style_table={'overflowX': 'auto'},
        sort_action="native",
        page_size=15, # Show 15 rows per page
        style_cell={'textAlign': 'left', 'backgroundColor': '#333333', 'color': 'white'},
        style_header={
            'backgroundColor': '#555555',
            'fontWeight': 'bold'
        },
    )
])

# This is the "magic" that connects components.
# It says: "When 'interval-component' ticks, update the 'data' of 'live-traffic-table'"
@app.callback(
    Output('live-traffic-table', 'data'),      # The component property to update
    Input('interval-component', 'n_intervals') # The component property that triggers
)
def update_table(n):
    try:
        # Read the log file into a pandas DataFrame
        df = pd.read_csv(LOG_FILE)
        
        # Get the last 50 rows and reverse them (newest on top)
        df_display = df.tail(50).iloc[::-1]
        
        # Convert the DataFrame to a dictionary format that Dash table understands
        return df_display.to_dict('records')
    
    except FileNotFoundError:
        return [] # Return empty list if file doesn't exist yet
    except pd.errors.EmptyDataError:
        return [] # Return empty list if file is empty (e.g., only has header)
    except Exception as e:
        print(f"Error reading log: {e}")
        return []

# --- Main part of the script ---
if __name__ == '__main__':
    print("🚀 Starting dashboard v0.1...")
    print("View at http://127.0.0.1:8050")
    # debug=True allows for auto-reloading if you change this script
    app.run(debug=True)
