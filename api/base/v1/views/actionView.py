from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from elasticsearch_dsl import Search
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.base.v1.Response import Response
from elasticsearch import Elasticsearch

from mqtt.publisher import RedisMQTT

publisher = RedisMQTT('localhost', 6379, 'localhost', 1883)


class ActionView(APIView):
    # permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="Register Api",
        responses={201: 'User is signed up', 406: 'data is wrong', 400: 'input data is empty'},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'action': openapi.Schema(type=openapi.TYPE_STRING, description='string', default="admin"),
            }
        ))
    def post(self, request):
        try:
            action = request.data.get('action')
            res = publisher.set_data('0001', action)
            if res:
                return Response(data={}, data_status=status.HTTP_200_OK,
                                message='set data  successfully',
                                status=status.HTTP_200_OK)
            else:
                return Response(data='set data failed', message='there some problem in your request',
                                data_status=status.HTTP_400_BAD_REQUEST, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data='set data failed', message=str(e),
                            data_status=status.HTTP_400_BAD_REQUEST, status=status.HTTP_200_OK)
