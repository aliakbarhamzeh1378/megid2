import paho.mqtt.client as mqtt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView

from api.base.v1.Response import Response
from mqtt.publisher import RedisMQTT


client = mqtt.Client()
client.connect('broker.emqx.io', 1883)


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
    def set_data(self, board_id, action_data: str):
        data = "000"
        if action_data.lower() == "water off":
            data = "000"
        elif action_data.lower() == "water on":
            data = "001"

        elif action_data.lower() == "light off":
            data = "010"

        elif action_data.lower() == "light on":
            data = "011"

        elif action_data.lower() == "fan off":
            data = "100"

        elif action_data.lower() == "fan on":
            data = "101"

        elif action_data.lower() == "heater off":
            data = "110"

        elif action_data.lower() == "heater on":
            data = "111"
        else:
            return False
        client.publish('TWF7GH/S:0001', data)
        return True

    def post(self, request):
        try:
            action = request.data.get('action')
            res = self.set_data('0001', action)
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
