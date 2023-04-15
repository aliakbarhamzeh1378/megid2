import time

from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from elasticsearch_dsl import Search
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.base.v1.Response import Response
from elasticsearch import Elasticsearch


# create an Elasticsearch client instance


class ReportDataView(APIView):
    # permission_classes = (    IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="Get Permission List Api",
        responses={201: 'Get data success',
                   400: 'Get data failed'},
    )
    def get(self, request):
        try:
            es = Elasticsearch()
            b = time.time()
            # specify the index name
            index_name = 'fluentd'
            # create a search request with a match_all query and sort by timestamp
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
                                        "gte": "2023-04-13",
                                        "lte": "2023-04-16"
                                    }
                                }
                            }
                        ]
                    }
                }
            }

            # execute the search query and retrieve all search hits
            scroll_size = 1000
            data = []
            results = es.search(index=index_name, body=query, scroll='2m', size=scroll_size)

            # keep scrolling until there are no more search hits
            while len(results['hits']['hits']) > 0:
                # do something with the search hits
                for hit in results['hits']['hits']:
                    data.append(hit['_source'])

                # get the next page of search hits using the scroll API
                scroll_id = results['_scroll_id']
                results = es.scroll(scroll_id=scroll_id, scroll='2m')

            return Response(data={'data': data, 'time_elapsed': time.time() - b}, data_status=status.HTTP_200_OK,
                            message='Get data  successfully',
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data='Get data failed', message=str(e),
                            data_status=status.HTTP_400_BAD_REQUEST, status=status.HTTP_200_OK)
