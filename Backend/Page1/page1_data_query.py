import couchdb.design
from datetime import datetime
import pandas as pd
import couchdb
import json
import os

city_names = ['1gsyd', '2gmel', '3gbri', '4gade', '5gper', '6ghob', '7gdar', '8acte']


def query_data(db):
    # Get the current file path
    current_path = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_path, 'page1_data.json')

    # Check if the file exists
    if os.path.exists(json_file_path):
        # If the file exists, load the data from the file
        with open(json_file_path, 'r') as infile:
            data_list = json.load(infile)
            print(f'Data loaded from file. {len(data_list)} lines in total.')
            return data_list
    else:
        # If the file does not exist, fetch the data and store it in the file
        data_list = []
        counter = 0

        for i in range(len(city_names)):
            city_name = city_names[i]
            view_results = db.view(f"_design/my_design_page1/_view/gcc_{city_name}")

            for row in view_results:
                data_out = {}
                row = row.value

                if 'sentiment' in list(row.keys()):
                    data_out['sentiment'] = row['sentiment']
                    data_out['loc'] = row['loc']
                    data_out['city'] = row['city']
                    data_out['datetime'] = row['datetime'][:-5]

                    data_list.append(data_out)
                    counter += 1

        # Store the data in the 'page1_data.json' file
        with open(json_file_path, 'w') as outfile:
            json.dump(data_list, outfile, ensure_ascii=False)

        print(f'Data done! {counter} lines in total.')
        return data_list


def main():
    query_data()


if __name__ == '__main__':
    main()
