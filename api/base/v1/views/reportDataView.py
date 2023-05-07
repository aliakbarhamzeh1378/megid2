import time

from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from elasticsearch_dsl import Search
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.base.v1.Response import Response
from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch()

# Set the number of results per section
section_size = 100


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
            sensor_name = request.query_params.get('sensor_id')
            if sensor_name is not None and request.user.Permissions.Access > 1:
                board_id = sensor_name
            else:
                board_id = str(request.user.Slave_id).split(',')[0]
            start = request.query_params.get('start', '2023-04-13')
            end = request.query_params.get('end', '2023-04-14')
            # specify the index name
            # Set up the search query
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    "slave_id": board_id
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

            data = []
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
                    data.append(hit['_source'])

            return Response(data={'data': data},
                            data_status=status.HTTP_200_OK,
                            message='Get data  successfully',
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data='Get data failed', message=str(e),
                            data_status=status.HTTP_400_BAD_REQUEST, status=status.HTTP_200_OK)
