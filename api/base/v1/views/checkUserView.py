from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView

from api.base.v1.Response import Response
from api.base.v1.models.userModel import UserModel


class CheckUserNameView(APIView):

    @swagger_auto_schema(
        operation_description="Check user exist Api",
        responses={202: 'User not exist', 406: 'User exist', 400: 'Username is empty'},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'Username': openapi.Schema(type=openapi.TYPE_STRING, description='string', default="admin"),
            }
        ))
    def post(self, request):
        try:
            Username = request.data['Username']
            check = UserModel.objects.filter(Username=Username)
            if len(check) != 0:

                return Response(data={'info': 'user exist', 'data': True}, data_status=status.HTTP_406_NOT_ACCEPTABLE,
                                message='user exist',
                                status=status.HTTP_200_OK)
            else:

                return Response(data={'info': 'user not exist', 'data': False}, data_status=status.HTTP_202_ACCEPTED,
                                message='user not exist',
                                status=status.HTTP_200_OK)


        except Exception as e:
            return Response(data=str(e), data_status=status.HTTP_400_BAD_REQUEST,
                            message='CheckUser Failed',
                            status=status.HTTP_200_OK)


class CheckEmailView(APIView):

    @swagger_auto_schema(
        operation_description="Check user email exist Api",
        responses={202: 'User not exist', 406: 'User exist', 400: 'Username is empty'},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'Email': openapi.Schema(type=openapi.TYPE_STRING, description='string', default="admin@admin.com"),
            }
        ))
    def post(self, request):
        try:
            Email = request.data['Email']
            check = UserModel.objects.filter(Email=Email)
            if len(check) != 0:

                return Response(data={'info': 'email exist', 'data': True}, data_status=status.HTTP_406_NOT_ACCEPTABLE,
                                message='email exist',
                                status=status.HTTP_200_OK)
            else:

                return Response(data={'info': 'email not exist', 'data': False}, data_status=status.HTTP_202_ACCEPTED,
                                message='email not exist',
                                status=status.HTTP_200_OK)


        except Exception as e:
            return Response(data=str(e), data_status=status.HTTP_400_BAD_REQUEST,
                            message='CheckUserEmail Failed',
                            status=status.HTTP_200_OK)
