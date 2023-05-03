import couchdb
import json
import time
# authentication
admin = 'admin'
password = 'password123456'
url = f'http://{admin}:{password}@172.26.128.204:5984/'
db = 'gcc_sentiment_data'
city_names = ['1gsyd', '2gmel', '3gbri', '4gade', '5gper', '6ghob', '7gdar', '8acte']
couch = couchdb.Server(url)
if db in couch:
    db = couch[db]


# 每页记录数
page_size = 10000
startkey = None
startkey_docid = None
with open("page1_data.json", "w") as outfile:
    start = time.time()
    counter = 0
    for i in range(len(city_names)):
        city_name = city_names[i]
        while True:
            # 使用startkey和startkey_docid参数进行分页查询
            view_results = db.view(f"_design/my_design_page1/_view/gcc_{city_name}", startkey=startkey, startkey_docid=startkey_docid, limit=page_size+1)
            results = list(view_results)
            # 处理查询结果
            for row in view_results:
                data_out = {}
                row = row.value
                if 'sentiment' in list(row.keys()):
                    data_out['sentiment'] = row['sentiment']
                    data_out['loc'] = row['loc']
                    data_out['city'] = row['city']
                    data_out['datetime'] = row['datetime'][:-5]
                    outfile.write(json.dumps(data_out, ensure_ascii=False))
                    outfile.write('\n')
                    counter += 1

            # 更新startkey和startkey_docid参数以获取下一页
            if len(results) > page_size:
                last_row = results[page_size]
                startkey = last_row.key
                startkey_docid = last_row.id
            else:
                break


print(f'use {time.time()-start} s. file done! {counter} lines in total.')
