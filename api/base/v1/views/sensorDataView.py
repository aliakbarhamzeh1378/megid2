from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from elasticsearch_dsl import Search
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.base.v1.Response import Response
from elasticsearch import Elasticsearch

from cas_server2.settings import Redis


# create an Elasticsearch client instance


class SensorDataView(APIView):
    # permission_classes = (    IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="Get Permission List Api",
        responses={201: 'Get data success',
                   400: 'Get data failed'},
    )
    def get(self, request):
        try:
            es = Elasticsearch()
            board_id = request.user.Slave_id
            if board_id is None:
                return Response(data='Get data failed', message="You dont have any slave id",
                                data_status=status.HTTP_400_BAD_REQUEST, status=status.HTTP_200_OK)
            # specify the index name
            index_name = 'fluentd'
            # create a search request with a match_all query and sort by timestamp
            search_request = {
                'query': {
                    "match": {
                        "slave_id": board_id
                    }
                },
                'sort': [
                    {
                        "time": {
                            'order': 'desc'
                        }
                    }
                ],
                'size': 1  # only retrieve the last item
            }

            # execute the search request
            search_results = es.search(index=index_name, body=search_request)

            # extract the hit from the search results
            hit = search_results['hits']['hits']
            # print(hit)
            hit = hit[0]

            # extract the source data from the hit
            source_data = hit['_source']
            a, b, c, d = Redis.get(str(board_id) + "_water"), Redis.get(str(board_id) + "_light"), Redis.get(
                str(board_id) + "_fan"), Redis.get(str(board_id) + "_heater")
            print(a, b, c, d)
            # print the source data for the last item
            #            print(source_data)

            return Response(data={
                'data': source_data,
                'water': a,
                'light': b,
                'fan': c,
                'heater': d
            }, data_status=status.HTTP_200_OK,
                message='Get data  successfully',
                status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data='Get data failed', message=str(e),
                            data_status=status.HTTP_400_BAD_REQUEST, status=status.HTTP_200_OK)
