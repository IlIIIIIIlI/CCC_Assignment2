import json
import csv

# Load the JSON data from a file or a string
with open('page2_data_Mastodon_single.json', 'r') as f:
    data = json.load(f)

# Extract the keys from the first object in the JSON data
keys = data[0].keys()

# Open a new CSV file and write the header row
with open('page2_data_Mastodon_single.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=keys)
    writer.writeheader()

    # Write each object in the JSON data as a row in the CSV file
    for row in data:
        writer.writerow(row)