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