import pandas as pd
import json
from loadData import read_data

with open('config.json', 'r') as f:
    config_data = json.load(f)
localhost = config_data['IP']
username = config_data['username']
password = config_data['password']

def get_database_name():
    return read_data(f"http://{username}:{password}@{localhost}/_all_dbs")
