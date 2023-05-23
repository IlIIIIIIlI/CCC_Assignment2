import json

with open("./Page2/page2_data_M.json", "r") as file:
    data = json.load(file)

def query_data():
    return data