import requests
import pandas as pd
from io import StringIO

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception("Failed to fetch data")

def process_data(raw_data):
    # Convert bytes to a string buffer
    string_data = StringIO(raw_data.decode('utf-8'))
    data = pd.read_csv(string_data)
    # Process the data as required
    return data

def get_processed_data(url):
    raw_data = fetch_data(url)
    processed_data = process_data(raw_data)
    return processed_data

def get_best_performers_by_points(df, num_weeks, positions):
    latest_gw = df['GW'].max()
    filtered_df = df[df['GW'] > latest_gw - num_weeks]

    filtered_df = filtered_df.sort_values(by='GW', ascending=False)

    # Assuming 'value' column represents the current value of the player
    # Group by player name, sum the total_points, and get the latest 'value'
    best_performers = (filtered_df.groupby(['name', 'position'])
                                   .agg(total_points=('total_points', 'sum'),
                                        value=('value', 'last'))
                                   .reset_index())

    # Filter by position if necessary
    best_performers = best_performers.sort_values(by=['position', 'total_points'], ascending=[True, False])
    return best_performers[best_performers['position'].isin(positions)].head(50)


def get_best_performers_by_value(df, num_weeks, positions):
    latest_gw = df['GW'].max()
    filtered_df = df[df['GW'] > latest_gw - num_weeks]

    filtered_df = filtered_df.sort_values(by='GW', ascending=False)

    # Group by player name and position, sum the total_points, and get the latest 'value'
    aggregated_df = (filtered_df.groupby(['name', 'position'])
                                 .agg(total_points=('total_points', 'sum'),
                                      value=('value', 'last'))
                                 .reset_index())

    # Calculate points per value (total points divided by current value)
    aggregated_df['points_value'] = aggregated_df['total_points'] / aggregated_df['value']
    aggregated_df['points_value'] = aggregated_df['points_value'].round(1)

    # Filter by position if necessary and sort by points per value
    best_value_performers = aggregated_df[aggregated_df['position'].isin(positions)]
    best_value_performers = best_value_performers.sort_values(by='points_value', ascending=False)
    
    return best_value_performers.head(50)



def get_largest_price_changes(df, num_weeks):
    latest_gw = df['GW'].max()
    start_gw = latest_gw - num_weeks

    # Compare values between start and latest GW
    start_values = df[df['GW'] == start_gw].set_index('name')['value']
    latest_values = df[df['GW'] == latest_gw].set_index('name')['value']

    price_changes = (latest_values - start_values).dropna().reset_index()
    price_changes.columns = ['name', 'price_change']
    return price_changes.sort_values(by='price_change', ascending=False)


def get_largest_ownership_changes(df, num_weeks):
    latest_gw = df['GW'].max()
    start_gw = latest_gw - num_weeks

    # Compare ownership between start and latest GW
    start_ownership = df[df['GW'] == start_gw].set_index('name')['selected']
    latest_ownership = df[df['GW'] == latest_gw].set_index('name')['selected']

    ownership_changes = (latest_ownership - start_ownership).dropna().reset_index()
    ownership_changes.columns = ['name', 'ownership_change']
    return ownership_changes.sort_values(by='ownership_change', ascending=False)
