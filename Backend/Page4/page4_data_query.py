import json
import os

import couchdb

# authentication
admin = 'admin'
password = 'password123456'
url = f'http://{admin}:{password}@172.26.128.204:5984/'

# get couchdb instance
couch = couchdb.Server(url)

topics = {
    "income": ["income", "earnings", "salary", "wages", "revenue", "paycheck"],
    "health": ["health", "wellness", "fitness", "nutrition", "medicine", "medical"],
    "education": ["education", "school", "university", "college", "learning", "teaching"],
    "social_relationship": ["relationship", "social", "friends", "family", "community", "network"],
    "culture_and_leisure": ["culture", "leisure", "art", "entertainment", "hobby", "travel"],
    "sense_of_security": ["security", "safety", "protection", "insurance", "stability", "well-being"],
    "environmental_protection": ["environment", "protection", "conservation", "sustainability", "ecology", "recycling"]
}

current_path = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_path, 'page4_data.json')


def get_combined_text_list_for_topic(db, topic):
    combined_text_list = []
    topic_related_docs = db.view(f'topic_related_docs/by_{topic}_token')

    for row in topic_related_docs:
        text = row.value
        combined_text_list.append(text)

    return combined_text_list


def save_combined_text_list_to_json(db):
    combined_text_dict = {}
    for topic in topics.keys():
        combined_text_list = get_combined_text_list_for_topic(db, topic)
        combined_text_dict[topic] = combined_text_list

    with open(json_file_path, "w") as file:
        json.dump(combined_text_dict, file)


def load_combined_text_list_from_json():
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as file:
            combined_text_dict = json.load(file)
        return combined_text_dict

    return {}


def query_data_page4(db):
    combined_text_dict = load_combined_text_list_from_json()

    if not combined_text_dict:
        save_combined_text_list_to_json(db)
        combined_text_dict = load_combined_text_list_from_json()

    print(f'Data for page 4 done!')
    return combined_text_dict
