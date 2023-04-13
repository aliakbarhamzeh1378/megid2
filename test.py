from elasticsearch import Elasticsearch

# Create an Elasticsearch client instance
es = Elasticsearch(host="178.63.147.27")
query = {
  "size": 0,
  "aggs": {
    "latest_by_slave_id": {
      "terms": {
        "field": "slave_id",
        "size": 10000
      },
      "aggs": {
        "latest_by_time": {
          "top_hits": {
            "size": 1,
            "sort": [
              {
                "time": {
                  "order": "desc"
                }
              }
            ]
          }
        }
      }
    }
  }
}


# Execute the query
response = es.search(index='fluentd', body=query)

# Extract the results
hits = response['aggregations']['latest_by_slave_id']['buckets']
for hit in hits:
    print(hit['latest_by_time']['hits']['hits'][0]['_source'])
