#ssh -i Demo1.pem ubuntu@172.26.128.204
#scp -i  Demo1.pem /Users/qin/Desktop/couchdb/Mastodon.py ubuntu@172.26.128.204:/home/ubuntu/pyfile
#nohup python3 Mastodon.py &
import couchdb
import os
import shutil
from mastodon import Mastodon, StreamListener
import json
from dateutil import parser
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
from scipy.special import softmax
import csv
import urllib.request
from concurrent.futures import ThreadPoolExecutor


folder_name = 'cardiffnlp'

if os.path.exists(folder_name):
    shutil.rmtree(folder_name)

def split_time_by_period(timestamp):
    dt = parser.parse(timestamp)
    hour = dt.hour

    if 3 < hour <= 11:
        period = "morning"
    elif 11 <= hour < 19:
        period = "afternoon"
    else:
        period = "evening"

    return period


def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)


task = 'sentiment'
MODEL = f"cardiffnlp/twitter-roberta-base-{task}"

tokenizer = AutoTokenizer.from_pretrained(MODEL)

labels = []
mapping_link = f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/{task}/mapping.txt"
with urllib.request.urlopen(mapping_link) as f:
    html = f.read().decode('utf-8').split("\n")
    csvreader = csv.reader(html, delimiter='\t')
labels = [row[1] for row in csvreader if len(row) > 1]

model = AutoModelForSequenceClassification.from_pretrained(MODEL)
model.save_pretrained(MODEL)

def sentiment_m1(text):
    max_length = 512
    text = preprocess(text)
    encoded_input = tokenizer(text, return_tensors='pt', max_length=max_length, truncation=True)
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    return labels[ranking[0]]

def stream_from_server(base_url, access_token):
    try:
        m = Mastodon(
            api_base_url=base_url,
            access_token=access_token
        )

        while True:
            try:
                m.stream_public(Listener())
            except Exception as e:
                print(f'Error in stream_public: {e}. Restarting...')
    except Exception as e:
        print(f'Error connecting to server {base_url}: {e}')


# authentication
url = 'http://admin:password123456@172.26.128.137:5984'

# get couchdb instance
couch = couchdb.Server(url)

# indicate the db name
db_name = 'mastodon2'

# if not exist, create one
if db_name not in couch:
    db = couch.create(db_name)
else:
    db = couch[db_name]



# listen on the timeline
class Listener(StreamListener):
    # called when receiving new post or status update
    def on_update(self, status):
        try:
            # Perform sentiment analysis
            sentiment_label = sentiment_m1(status['content'])

            # Skip if sentiment is 'neutral'
            if sentiment_label == 'neutral':
                return

            # Keep only the relevant fields
            processed_status = {
                'id': status['id'],
                'created_at': status['created_at'],
                'content': status['content'],
                'username': status['account']['username'],
                'display_name': status['account']['display_name'],
                'acct': status['account']['acct'],
                'url': status['url'],
                'sentiment': sentiment_label
            }

            # Save to CouchDB
            json_str = json.dumps(processed_status, indent=2, sort_keys=True, default=str)
            doc_id, doc_rev = db.save(json.loads(json_str))
            print(f'Document saved with ID: {doc_id} and revision: {doc_rev}')
        except Exception as e:
            print(f'Error uploading document to CouchDB: {e}')

servers = [
    {
        'base_url': 'https://mastodon.au/',
        'access_token': 'zMfyrrco_Ma8zb5hkphxkqqLLWG9lNMSnix6mdw68vo'
    },
    {
        'base_url': 'https://aus.social/',
        'access_token': '5sHBCOygBtBjsdAcMmzMbGSPEWEQSDnj17NLHT7tNYA'
    }
]
try:
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(stream_from_server, server['base_url'], server['access_token']) for server in servers]
except Exception as e:
    print(f'Error running threads: {e}')
