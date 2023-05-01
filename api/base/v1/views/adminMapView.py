from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from elasticsearch_dsl import Search
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.base.v1.Response import Response
from elasticsearch import Elasticsearch


# create an Elasticsearch client instance


class AdminMapView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="Get Permission List Api",
        responses={201: 'Get data success',
                   400: 'Get data failed'},
    )
    def get(self, request):
        a = request.user.Permissions.Access
        if request.user.Permissions.Access < 2:
            return Response(data='Access Denied', message='Access Denied',
                            data_status=status.HTTP_403_FORBIDDEN, status=status.HTTP_200_OK)
        try:
            es = Elasticsearch()

            # specify the index name
            index_name = 'fluentd'
            # create a search request with a match_all query and sort by timestamp

            search_request = {
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
            if request.user.Permissions.Access == 2:
                search_request['aggs']['latest_by_slave_id']['terms']['include'] = str(request.user.Slave_id).split(",")

            # execute the search request
            search_results = es.search(index=index_name, body=search_request)

            # hits
            data = []
            hits = search_results['aggregations']['latest_by_slave_id']['buckets']
            for hit in hits:
                data.append(hit['latest_by_time']['hits']['hits'][0]['_source'])

            return Response(data=data, data_status=status.HTTP_200_OK,
                            message='Get data  successfully',
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data='Get data failed', message=str(e),
                            data_status=status.HTTP_400_BAD_REQUEST, status=status.HTTP_200_OK)
