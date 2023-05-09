import couchdb.design
from datetime import datetime
import pandas as pd
import couchdb
import json
import os
import requests



def query_data(db):
    # Get the current file path
    current_path = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_path, 'page2_data_M.json')

    
    preurl="http://admin:password123456@172.26.128.137:5984/mastodon2/_design/mas/_view/top?group=true&&reduce=true&descending=true"
    
    # Make the HTTP request to the view
    response = requests.get(preurl)

    # Parse the JSON response
    result = json.loads(response.text)

    # Print the top 10 authors with the most entries

    sorted_list = sorted(result['rows'], key=lambda x: x['value'], reverse=True)

    top_10_items = sorted_list[:10]

    print(top_10_items)

        # If the file does not exist, fetch the data and store it in the file
    data_list = []
    Aname="i['key']"
    num_M=0
    counter = 0
    rank=10
    for i in top_10_items:
        print(i)
        rank_name = rank
        rank-=1
        Aname=i['key']
        print(Aname)
        num_M=i['value']
        view_results = db.view(f"_design/mas/_view/full")
        
        for row in view_results:
            data_out = {}
            # print(rank_name)
            if(row.key==Aname):
            # print(row.id)
                row = row.value
            
                data_out['rank'] = rank_name
                data_out['username'] = row['username']
                data_out['totalM'] = num_M
                data_out['content'] = row['content']
                data_out['created_at'] = row['created_at']
                data_out['date'] = row['created_at'][:10]
                data_out['time'] = row['created_at'][12:-6]
                data_out['display_name'] = row['display_name']
                data_out['favourites_count'] = row['favourites_count']
                data_out['followers_count'] = row['followers_count']
                data_out['following_count'] = row['following_count']
                data_out['reblogs_count'] = row['reblogs_count']
                data_out['replies_count'] = row['replies_count']
                data_out['sensitive'] = row['sensitive']
                data_out['sentiment'] = row['sentiment']
                data_out['url'] = row['url']
                data_out['class']="mastodon"
                

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
    url = f'http://{admin}:{password}@172.26.128.137:5984/'
    db = 'mastodon2'
    couch = couchdb.Server(url)
    if db in couch:
        db = couch[db]
    return db
def main():
   

    db = login_to_db()
    query_data(db)


if __name__ == '__main__':
    main()
