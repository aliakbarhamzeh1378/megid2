from elasticsearch import Elasticsearch



es = Elasticsearch()

# specify the index name
index_name = 'logstash-2023.04.10'
# create a search request with a match_all query and sort by timestamp
search_request = {
'query': {
    "match": {
        "slave_id": "0001"
    }
},
'sort': [
    {
        "@timestamp": {
            'order': 'desc'
        }
    }
],
'size': 1  # only retrieve the last item
}

# execute the search request
search_results = es.search(index=index_name, body=search_request)

# extract the hit from the search results
hit = search_results['hits']['hits'][0]

# extract the source data from the hit
source_data = hit['_source']

# print the source data for the last item
print(source_data)
