from elasticsearch import helpers
from elasticsearch import Elasticsearch

es = Elasticsearch()

# Set the number of results per section
section_size = 100

# Get the start and end dates from the request parameters
start = '2023-04-13'
end =  '2023-04-14'


# Set up the search query
query = {
    "query": {
        "bool": {
            "must": [
                {
                    "match": {
                        "slave_id": "0001"
                    }
                },
                {
                    "range": {
                        "time": {
                            "gte": start,
                            "lte": end
                        }
                    }
                }
            ]
        }
    }
}

# Use the helpers.scan method to iterate over all results
for i, hit in enumerate(helpers.scan(
    es,
    query=query,
    index='fluentd',
    scroll='2m',
    size=section_size
)):
    # Print the first item of each section
    if i % section_size == 0:
        print(hit['_source'])
