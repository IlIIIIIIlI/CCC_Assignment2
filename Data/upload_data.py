import couchdb
import json

# authentication
admin = 'admin'
password = 'password123456'
url = f'http://{admin}:{password}@172.26.128.204:5984/'

# get couchdb instance
couch = couchdb.Server(url)

# indicate the db name
db_name = 'GCC_data'

# if not exist, create one
if db_name not in couch:
    db = couch.create(db_name)
else:
    db = couch[db_name]

# data to be stored
# Load the JSON file
with open('demo.json', 'r') as f:
    # 跳过第一行
    f.readline()
    # 逐行读取并解析 JSON
    counter = 1
    for line in f:
        # 最后一行不处理
        if line[0] == ']':
            continue
        # 倒数第二行不处理，其他的去掉逗号和换行符
        if line[-2] != '}':
            line = line[:-2]
        data = json.loads(line)
        db.save(data)
        # print(counter)
        counter += 1
print('All data have been saved!')
