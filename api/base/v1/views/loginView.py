from django.contrib.auth import authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from api.base.v1.Response import Response
from api.base.v1.serializers.userSerializer import UserSerializer


class LoginView(APIView):
    def token_generator(self, user):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    @swagger_auto_schema(
        operation_description="Login Api",
        responses={201: 'User is logged in', 404: 'Username or password was wrong',
                   400: 'Username or password is empty'},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'Username': openapi.Schema(type=openapi.TYPE_STRING, description='string', default="admin"),
                'Password': openapi.Schema(type=openapi.TYPE_STRING, description='string', default="13781211"),
            }
        ))
    def post(self, request):
        try:
            username = request.data.get("Username")
            if username is None:
                username = request.data.get("Email")
            password = request.data.get("Password")
            user = authenticate(username=username, password=password)
            serializer = UserSerializer(user)
            if user is None:

                return Response(data='Login failed', message="Username or password is wrong",
                                data_status=status.HTTP_401_UNAUTHORIZED, status=status.HTTP_200_OK)
            else:
                token = self.token_generator(user)
                return Response(data={'token': token,
                                      'userInfo':serializer.data}, data_status=status.HTTP_200_OK,
                                message='user was login successfully',
                                status=status.HTTP_200_OK)

        except Exception as e:
            return Response(data='Login failed', message=str(e),
                            data_status=status.HTTP_400_BAD_REQUEST, status=status.HTTP_200_OK)
