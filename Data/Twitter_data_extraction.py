import json
import ijson


city_file = 'sal.json'
file_name = 'mnt/ext100/twitter-huge.json'
city_dict = {}

def whether_process(full_name, city_dict):
    out = False
    wrong_list = ['australia', 'new south wales', 'queensland', 'victoria', 'western australia', 'south australia',
                  'tasmania',
                  '	australian capital territory', 'northern territory']
    if full_name not in wrong_list:
        if full_name in city_dict.keys():
            out = True
    return out

# Load city data
with open(city_file, 'r', encoding='utf-8') as sal_file:
    for prefix, event, value in ijson.parse(sal_file):
        if prefix.endswith('.gcc'):
            location = prefix.split('.')[0]
            if value[1] == 'g' or value == '8acte':
                city_dict[location] = value


with open(file_name, 'r') as f_in, open("demo.json", "w") as outfile:
    f_in.readline()
    counter = 1
    for line in f_in:
        if line[0] == ']':
            continue
        if line[-2] != '}':
            line = line[:-2]
        data = json.loads(line)
        loc = data['doc'].get('includes', {})
        if loc != {} and type(loc) != list:
            # if counter % 100000 == 0:
            #     print(counter)
            counter += 1
            full_name = loc.get('places')[0].get("full_name")
            full_name = full_name.split(',')[0].lower()
            if whether_process(full_name, city_dict):
                city = city_dict[full_name]
            new_data = {
            'id' : data['doc']['data']['author_id'],
            'GCC' : city,
            'text': data['doc']['data']['text'],
            'value': data['value'],
            'author_id': data['doc']['data']['author_id'],
            'context_annotations': data['doc']['data'].get('context_annotations', {}),
            'created_at': data['doc']['data']['created_at'],
            'public_metrics': data['doc']['data']['public_metrics'],
            'includes': data['doc'].get('includes', {}),
            'lang': data['doc']['data']['lang'],
            'matching_rules': data['doc']['matching_rules']
            }
            outfile.write(json.dumps(new_data, ensure_ascii=False))
            outfile.write('\n')
    # print(f'There are {counter} records.')