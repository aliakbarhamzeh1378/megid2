from datetime import datetime

from django.contrib.auth import authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from rest_framework import status

from api.base.v1.Response import Response
from api.base.v1.models.permisionsModel import PermissionModel
from api.base.v1.models.userModel import UserModel
from api.base.v1.serializers.userSerializer import UserSerializer


class RegisterView(APIView):
    def token_generator(self, user):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    @swagger_auto_schema(
        operation_description="Register Api",
        responses={201: 'User is signed up', 406: 'data is wrong', 400: 'input data is empty'},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'Username': openapi.Schema(type=openapi.TYPE_STRING, description='string', default="admin"),
                'Password': openapi.Schema(type=openapi.TYPE_STRING, description='string', default="13781211"),
                'Email': openapi.Schema(type=openapi.TYPE_STRING, description='string', default='admin1@gmail.com'),
            }
        ))
    def post(self, request):
        try:
            req = request.data.copy()
            req['DateJoin'] = datetime.now()
            req['LastLogin'] = datetime.now()

            account = UserModel.objects.create_user(
                Email=req['Email'],
                password=req['Password'],
                Username=req['Username'],
                date_joined=req['DateJoin'],
                last_login=req['LastLogin'],
                Permissions= PermissionModel.objects.get(Access=1)
            )
            token = self.token_generator(account)
            return Response(data={'token': token, 'userid': account.id, 'permission': account.Permissions},
                            data_status=status.HTTP_201_CREATED,
                            message='successfully registered new user.',
                            status=status.HTTP_200_OK)



        except Exception as e:

            return Response(data=str(e), data_status=status.HTTP_400_BAD_REQUEST,
                            message='Register failed',
                            status=status.HTTP_200_OK)
