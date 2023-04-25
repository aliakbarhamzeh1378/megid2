from django.contrib.auth import authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from api.base.v1.Response import Response
from api.base.v1.models.permisionsModel import PermissionModel
from api.base.v1.models.userModel import UserModel
from api.base.v1.serializers.userSerializer import UserSerializer, PermissionSerializer


class PermissionView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="Get Permission List Api",
        responses={201: 'Get data success',
                   400: 'Get data failed'},
      )
    def get(self, request):
        try:
            permissions = PermissionModel.objects.filter()
            serializer = PermissionSerializer(permissions, many=True)
            return Response(data=serializer.data, data_status=status.HTTP_201_CREATED,
                            message='Get data  successfully',
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data='Get data failed', message=str(e),
                            data_status=status.HTTP_400_BAD_REQUEST, status=status.HTTP_200_OK)
