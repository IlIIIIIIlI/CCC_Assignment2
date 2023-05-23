import couchdb
import datetime
import json

couch = couchdb.Server('http://admin:password123456@172.26.128.137:5984')  # or your server URL
db = couch['mastodon2']  # replace with your db name

result = db.view('view_design_doc/daily_counts', group=True)


def query_data(db):
    # Get today's date
    today = datetime.date.today()

    # Define the start date as May 9th of the current year
    start_date = datetime.date(today.year, 5, 9)

    # Create a counter for the cumulative results
    cumulative_count = 0

    # Create an empty dictionary to store the results
    results_dict = {}

    for row in result:
        # Parse the date from the key
        date = datetime.datetime.strptime(row.key, "%Y-%m-%d").date()

        # Check if the date is between the start date and today
        if start_date <= date <= today:
            # If it is, add the value to the cumulative count
            cumulative_count += row.value

            # Add the cumulative count to the dictionary
            results_dict[row.key] = {'count': row.value, 'cumulative_count': cumulative_count}

    print('end')
    return results_dict
