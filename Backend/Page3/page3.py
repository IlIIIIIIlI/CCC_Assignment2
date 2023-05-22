import os

import couchdb.design
from datetime import datetime
import couchdb
import csv
import json

# authentication
# admin = 'admin'
# password = 'password123456'
# url = f'http://{admin}:{password}@172.26.128.204:5984/'
# db = 'gcc_sentiment_data'
city_names = ['1gsyd', '2gmel', '3gbri', '4gade', '5gper', '6ghob', '7gdar', '8acte']
# couch = couchdb.Server(url)
# if db in couch:
#     db = couch[db]
token = ["marriage", "wedding", "bride", "groom", "husband", "wife", "spouse", "marriage certificate", "engagement",
         "fiancé", "fiancée", "matrimony", "honeymoon", "anniversary", "divorce", "separation", "marital status",
         "marital vows", "marriage counseling", "marriage ceremony", "marriage proposal", "wedding ring",
         "wedding reception", "wedding dress", "wedding vows"]
token2 = ["earnings", "revenue", "salary", "wage", "paycheck", "compensation", "profit", "gross income", "net income",
          "disposable income", "fixed income", "passive income", "investment income", "income tax", "income statement",
          "income inequality", "income bracket", "household income", "personal income", "business income",
          "unearned income", "taxable income", "earned income", "income stream", "income source", "median income",
          "high-income", "low-income", "middle-income", "supplemental income"]
token3 = ["rent", "apartment", "house", "property", "lease", "tenant", "landlord", "rental", "roommate", "sublet",
          "deposit", "utilities", "furnished", "unfurnished", "lease agreement", "rental agreement",
          "rental application", "eviction", "notice", "inspection", "maintenance", "security deposit",
          "rent increase", "rental market", "rental property", "rental cost", "lease term", "rental contract",
          "rental period", "rental agency"]
# query data from couchDB
topics = ['marriage', 'income', 'rent']
tokens = [token, token2, token3]


def query_data(db):
    # Get the current file path
    current_path = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_path, 'page3_data.json')

    # Check if the file exists
    if os.path.exists(json_file_path):
        # If the file exists, load the data from the file
        with open(json_file_path, 'r') as infile:
            data_list = json.load(infile)
            print(f'Data loaded from file. {len(data_list)} lines in total.')
            return data_list
    else:
        # If the file does not exist, fetch the data and store it in the file
        data = []
        for i in range(len(city_names)):
            city_name = city_names[i]
            view_results = db.view(f"_design/my_design_page1/_view/gcc_{city_name}")
            data_out = {'city': city_name}
            for topic in range(3):
                counter = 0
                positive = 0
                data_out[f'{topics[topic]}_count'] = 0
                for row in view_results:
                    row = row.value
                    if 'text' in list(row.keys()) and 'sentiment' in list(row.keys()):
                        text = row["text"].lower()
                        # print(text)
                        for t in tokens[topic]:
                            if t in text:
                                data_out[f'{topics[topic]}_count'] += 1
                                counter += 1
                                if row['sentiment'] == 'positive':
                                    positive += 1
                data_out[f'{topics[topic]}_positive_rate'] = positive / counter
            data.append(data_out)

        with open(json_file_path, 'w') as outfile:
            json.dump(data, outfile, ensure_ascii=False)

        print(f'Data for page 3 done!')
        return data

# data = []
# for i in range(len(city_names)):
#     city_name = city_names[i]
#     view_results = db.view(f"_design/my_design_page1/_view/gcc_{city_name}")
#     data_out = {'city': city_name}
#     for topic in range(3):
#         counter = 0
#         positive = 0
#         data_out[f'{topics[topic]}_count'] = 0
#         for row in view_results:
#             row = row.value
#             if 'text' in list(row.keys()) and 'sentiment' in list(row.keys()):
#                 text = row["text"].lower()
#                 # print(text)
#                 for t in tokens[topic]:
#                     if t in text:
#                         data_out[f'{topics[topic]}_count'] += 1
#                         counter += 1
#                         if row['sentiment'] == 'positive':
#                             positive += 1
#         data_out[f'{topics[topic]}_positive_rate'] = positive/counter
#     data.append(data_out)
# csv_file = f"page3-data.csv"
#
# fields = ["city", "marriage_count", "marriage_positive_rate", "income_count", "income_positive_rate",
#           "rent_count", "rent_positive_rate"]
#
# with open(csv_file, mode="w", newline="") as file:
#     writer = csv.DictWriter(file, fieldnames=fields)
#     writer.writeheader()
#     writer.writerows(data)
# print(f'{csv_file} finished!')
