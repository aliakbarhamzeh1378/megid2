import time
from datetime import datetime, timedelta

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# create an Elasticsearch client instance
es = Elasticsearch()

# specify the index name
index_name = 'logstash-2023.04.10'
# define the index mapping
# get the current time
current_time = datetime.now()

# define the time interval for the search
time_window = timedelta(minutes=5)

# calculate the start and end times for the search interval
start_time = current_time - time_window
end_time = current_time + time_window

# specify the search query
search_query = {
    "query": {
        "match_all": {}
    },
    "sort": [
        {
            "@timestamp": {
                "order": "desc"
            }
        }
    ],
    "size": 1
}


for i in range(0,1000):
    # execute the search query
    search_result = es.search(index=index_name, body=search_query)

    # extract the hit from the search result
    hit = search_result['hits']['hits'][0]

    # do something with the hit
    print(hit['_source'])
    time.sleep(2)