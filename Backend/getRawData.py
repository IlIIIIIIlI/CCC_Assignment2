import pandas as pd
import json
from loadData import read_data

f = open('config.json')
localhost = json.load(f)['IP']


def get_database_name():
    return read_data(f"http://admin:password123456@{localhost}/_all_dbs")
