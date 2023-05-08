import couchdb.design
from datetime import datetime
import pandas as pd
import couchdb
import json
import os

tweet_rank = ['top1', 'top2', 'top3', 'top4', 'top5', 'top6', 'top7', 'top8','top9', 'top10']


def query_data(db):
    # Get the current file path
    current_path = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_path, 'page2_data.json')

    # Check if the file exists
    if os.path.exists(json_file_path):
        # If the file exists, load the data from the file
        
        with open(json_file_path, 'r') as infile:
            data_list = json.load(infile)
            if len(data_list)>46711:
                print(f'Data loaded from file. {len(data_list)} lines in total.')
                return data_list
            else:
                # If the file does not exist, fetch the data and store it in the file
                data_list = []
                
                counter = 0
                for i in range(len(tweet_rank)):
                    rank_name = tweet_rank[i]
                    view_results = db.view(f"_design/test1/_view/{rank_name}")
                
                    for row in view_results:
                        data_out = {}
                        # print(rank_name)
                    
                        # print(row.id)
                        row = row.value
                        
                        try:
                            data_out['rank'] = rank_name
                            data_out['author_id'] = row['author_id']
                            
                            data_out['text'] = row['text']
                            data_out['created_at'] = row['created_at']
                            data_out['date'] = row['created_at'][:10]
                            data_out['time'] = row['created_at'][12:-5]
                            data_out['author_name'] = row['author_name']
                            data_out['url'] = row['url']
                            
                            data_out['sentiment'] = row['sentiment']
                            data_out['class']="mastodon"
                        
                        except KeyError:
                            continue
                        

                        data_list.append(data_out)
                        counter += 1

                # Store the data in the 'page1_data.json' file
                # Read the existing JSON data from the file
                with open(json_file_path, 'r') as f:
                    existing_data = json.load(f)

                # Add new data to the existing data
                new_data = data_list
                existing_data.extend(new_data)

                # Write the updated data back to the file
                with open(json_file_path, 'w') as f:
                    json.dump(existing_data, f,ensure_ascii=False)



            

                print(f'Data done! {counter} lines in total.')
                return data_list

 # authentication
def login_to_db():
    admin = 'admin'
    password = 'password123456'
    url = f'http://{admin}:{password}@172.26.128.137:5984/'
    db = 'mastodon'
    couch = couchdb.Server(url)
    if db in couch:
        db = couch[db]
    return db
def main():
   

    db = login_to_db()
    query_data(db)


if __name__ == '__main__':
    main()
