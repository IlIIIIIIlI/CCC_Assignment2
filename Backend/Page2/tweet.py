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
    json_file_path = os.path.join(current_path, 'page2_data_T.json')

    
    preurl="http://admin:password123456@172.26.128.204:5984/gcc_sentiment_data/_design/view1/_view/top?group=true&&reduce=true&descending=true"
    
    # Make the HTTP request to the view
    response = requests.get(preurl)

    # Parse the JSON response
    result = json.loads(response.text)

    # Print the top 10 authors with the most entries

    sorted_list = sorted(result['rows'], key=lambda x: x['value'], reverse=True)

    top_10_items = sorted_list[:10]
    print("haha")
    print(top_10_items)

        # If the file does not exist, fetch the data and store it in the file
    data_list = []
    Aname="i['key']"
    num_M=0
    counter = 0
    rank=1
    for i in top_10_items:
        print(i)
        rank_name = "top"+str(rank)
        rank+=1
        Aname=i['key']
        print(Aname)
        num_M=i['value']
        view_results = db.view(f"_design/view1/_view/full")
        
        for row in view_results:
            data_out = {}
            # print(rank_name)
            if(row.key==Aname):
            # print(row.id)
                row = row.value
            
                data_out['rank'] = rank_name
                if row['author_id']=='1423662808311287813':
                    data_out['author_id'] = 'VIKING 🖤⚔️🗡️'
                elif row['author_id']=='820431428835885059':
                    data_out['author_id'] = '🇦🇺mikeaubrey🏳️‍🌈'
                elif row['author_id']=='826332877457481728':
                    data_out['author_id'] = 'Lady Pooh ( Crazy Sewer Rat )'
                elif row['author_id']=='1225473612167016449':
                    data_out['author_id'] = 'Antisocial'
                elif row['author_id']=='823550539':
                    data_out['author_id'] = 'david edgerton'
                elif row['author_id']=='1250331934242123776':
                    data_out['author_id'] = 'Dr Mark | 北马克 | 🍊🐰🇵🇸🏴'
                elif row['author_id']=='1381214332114010114':
                    data_out['author_id'] = 'Lourdes Cobberwealth & Sanctuary🐪❤️'
                elif row['author_id']=='1369912352133373955':
                    data_out['author_id'] = 'Laura O Brien'
                elif row['author_id']=='1264385409754132480':
                    data_out['author_id'] = 'Megan peach'
                elif row['author_id']=='2596393884':
                    data_out['author_id'] = 'Casey K'

                data_out['GCC'] = row['GCC']
                data_out['loc'] = row.get('full_name',0)
                data_out['bbox'] = row.get('bbox',0)

                data_out['text'] = row['text']
                data_out['tokens'] = row.get('tokens',0)
                data_out['created_at'] = row['created_at']
                data_out['date'] = row['created_at'][:10]
                data_out['time'] = row['created_at'][12:-5]

                data_out['retweet_count'] = row.get('retweet_count',0)
                data_out['reply_count'] = row.get('reply_count',0)
                data_out['like_count'] = row.get('like_count',0)
                data_out['quote_count'] = row.get('quote_count',0)
                data_out['time_period'] = row.get('time_period',0)
                data_out['sentiment'] = row.get('sentiment',0)
                data_out['class']="tweet"
                
                

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
