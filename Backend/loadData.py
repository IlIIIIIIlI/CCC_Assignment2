import requests
import json

f = open('config.json')
localhost = json.load(f)['IP']


def read_data(command):
    r = requests.get(command)
    r = r.json()
    return r

if __name__ == '__main__':
    print(read_data(
        f"http://admin:password123456@{localhost}/_all_dbs"))
