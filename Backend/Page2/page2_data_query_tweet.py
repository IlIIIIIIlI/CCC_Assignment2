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
    json_file_path = os.path.join(current_path, 'page2_data_T.json')

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
        for i in range(len(tweet_rank)):
            rank_name = tweet_rank[i]
            view_results = db.view(f"_design/view1/_view/{rank_name}")
           
            for row in view_results:
                data_out = {}
                # print(rank_name)
               
                # print(row.id)
                row = row.value
                
                try:
                    data_out['rank'] = rank_name
                    data_out['author_id'] = row['author_id']
                    data_out['GCC'] = row['GCC']
                    
                    
                    data_out['loc'] = row['full_name']
                    data_out['bbox'] = row['bbox']
                    data_out['text'] = row['text']
                    data_out['tokens'] = row['tokens']
                    data_out['created_at'] = row['created_at']
                    data_out['date'] = row['created_at'][:10]
                    data_out['time'] = row['created_at'][12:-5]
                    data_out['retweet_count'] = row['retweet_count']
                    data_out['reply_count'] = row['reply_count']
                    data_out['like_count'] = row['like_count']
                    data_out['quote_count'] = row['quote_count']
                    data_out['time_period'] = row['time_period']
                    data_out['sentiment'] = row['sentiment']
                    data_out['class']="tweet"
                
                except KeyError:
                    continue
                

                data_list.append(data_out)
                counter += 1

        # Store the data in the 'page1_data.json' file
        with open(json_file_path, 'w') as outfile:
            json.dump(data_list, outfile, ensure_ascii=False)

        print(f'Data done! {counter} lines in total.')
        return data_list

 # authentication
def login_to_db():
    admin = 'admin'
    password = 'password123456'
    url = f'http://{admin}:{password}@172.26.128.204:5984/'
    db = 'gcc_sentiment_data'
    couch = couchdb.Server(url)
    if db in couch:
        db = couch[db]
    return db
def main():
   

    db = login_to_db()
    query_data(db)


if __name__ == '__main__':
    main()
