import requests
import json

with open('config.json', 'r') as f:
    config_data = json.load(f)
localhost = config_data['IP']
username = config_data['username']
password = config_data['password']


def read_data(command):
    r = requests.get(command)
    r = r.json()
    return r

if __name__ == '__main__':
    print(read_data(
        f"http://{username}:{password}@{localhost}/_all_dbs"))
