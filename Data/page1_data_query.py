import couchdb.design
from datetime import datetime
import json
import couchdb

# authentication
admin = 'admin'
password = 'password123456'
url = f'http://{admin}:{password}@172.26.128.204:5984/'
db = 'gcc_sentiment_data'
city_names = ['1gsyd', '2gmel', '3gbri', '4gade', '5gper', '6ghob', '7gdar', '8acte']
couch = couchdb.Server(url)
if db in couch:
    db = couch[db]

# query data from couchDB

with open("page1_data.json", "w") as outfile:
    for i in range(len(city_names)):
        data_out = {'sentiment': [], 'loc': [], 'datetime': [], 'city': []}
        city_name = city_names[i]
        view_results = db.view(f"_design/my_design_page1/_view/gcc_{city_name}")
        for row in view_results:
            row = row.value
            try:
                if 'sentiment' in list(row.keys()):
                    data_out['sentiment'] = row['sentiment']
                    data_out['loc'] = row['loc']
                    data_out['city'] = row['city']
                    format = "%Y-%m-%dT%H:%M:%S"
                    date = datetime.strptime(row['datetime'][:-5], format)
                    data_out['datetime'] = date
            except KeyError and ValueError:
                # Ignore the KeyError and continue with the next iteration of the loop
                continue
        outfile.write(json.dumps(data_out, ensure_ascii=False))
        outfile.write('\n')
print(f'file done!')
