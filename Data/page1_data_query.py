import couchdb.design
from datetime import datetime
import pandas as pd
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
data_out = {'sentiment' : [], 'loc' : [], 'datetime' : [], 'city' : []}
for i in range(len(city_names)):
    city_name = city_names[i]
    view_results = db.view(f"_design/my_design_page1/_view/gcc_{city_name}")
    for row in view_results:
        row = row.value
        try:
            if 'sentiment' in list(row.keys()):
                data_out['sentiment'].append(row['sentiment'])
                data_out['loc'].append(row['loc'])
                data_out['city'].append(row['city'])
                format = "%Y-%m-%dT%H:%M:%S"
                date = datetime.strptime(row['datetime'][:-5], format)
                data_out['datetime'].append(date)
        except KeyError and ValueError:
            # Ignore the KeyError and continue with the next iteration of the loop
            continue
df = pd.DataFrame(data_out)
df.to_csv(f'page1_data.csv')
print(f'file done!')
