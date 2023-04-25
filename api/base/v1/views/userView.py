from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.base.v1.Response import Response
from api.base.v1.models.permisionsModel import PermissionModel
from api.base.v1.models.userModel import UserModel
from api.base.v1.serializers.userSerializer import UserSerializer


class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="Get User List Api",
        responses={201: 'Get data success',
                   400: 'Get data failed'},
    )
    def get(self, request):
        try:
            users = UserModel.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(data=serializer.data, data_status=status.HTTP_201_CREATED,
                            message='Get data  successfully',
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data='Get data failed', message=str(e),
                            data_status=status.HTTP_400_BAD_REQUEST, status=status.HTTP_200_OK)

    def put(self, request):
        try:
            user_id = request.data.get('user_id')
            if user_id == None:
                return Response(data='user not found', message=str('user not found'),
                                data_status=status.HTTP_404_NOT_FOUND, status=status.HTTP_200_OK)
            user = UserModel.objects.get(pk=int(user_id))
            if user == None:
                return Response(data='user not found', message=str('user not found'),
                                data_status=status.HTTP_404_NOT_FOUND, status=status.HTTP_200_OK)
            Email = request.data.get('email')
            Username = request.data.get('username')
            Slave_id = request.data.get('slave_id')
            Permission = request.data.get('permission')
            data = {}
            if Email is not None:
                user.Email = Email

            if Username is not None:
                user.Username = Username

            if Slave_id is not None:
                user.Slave_id = Slave_id

            if Permission is not None:
                user.Permissions = PermissionModel.objects.get(Access=int(Permission))
            user.save()
            return Response(data={}, data_status=status.HTTP_201_CREATED,
                            message='Get data  successfully',
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data='Get data failed', message=str(e),
                            data_status=status.HTTP_400_BAD_REQUEST, status=status.HTTP_200_OK)
