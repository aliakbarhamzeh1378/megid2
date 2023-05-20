from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from greenhouse.base.v1.models.logicModel import LogicModel
from greenhouse.base.v1.serializers.logicSerializer import LogicSerializer


class LogicModelDetail(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="Get all sensor data",
        responses={
            200: openapi.Response(
                description="OK",
                schema=LogicSerializer(many=True)
            ),
        }
    )
    def get(self, request, pk):
        try:
            sensor_data = LogicModel.objects.get(pk=pk, user=request.user)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = LogicSerializer(sensor_data)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update an existing sensor data",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'sensor_name': openapi.Schema(type=openapi.TYPE_STRING),
                'data_json': openapi.Schema(type=openapi.TYPE_OBJECT),
            }
        ),
        responses={
            200: openapi.Response(
                description="OK",
                schema=LogicSerializer
            ),
            400: "Bad Request",
            404: "Not Found"
        }
    )
    def put(self, request, pk):
        try:
            sensor_data = LogicModel.objects.get(pk=pk, user=request.user)
        except LogicModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = request.data
        data['user'] = request.user.pk

        serializer = LogicSerializer(sensor_data, data=request.data)
        if serializer.is_valid():
            sensor_data = serializer.save()
            return Response(LogicSerializer(sensor_data).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete an existing sensor data",
        responses={
            204: "No Content",
            404: "Not Found"
        }
    )
    def delete(self, request, pk):
        try:
            sensor_data = LogicModel.objects.get(pk=pk, user=request.user)
        except LogicModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        sensor_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LogicModelList(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="Get all sensor data",
        responses={
            200: openapi.Response(
                description="OK",
                schema=LogicSerializer(many=True)
            )

        },
        security=[{"Bearer": []}]
    )
    def get(self, request):
        sensor_data = LogicModel.objects.filter(user=request.user)
        serializer = LogicSerializer(sensor_data, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new sensor data",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'sensor_name': openapi.Schema(type=openapi.TYPE_STRING),
                'data_json': openapi.Schema(type=openapi.TYPE_OBJECT),
            }
        ),
        responses={
            201: openapi.Response(
                description="Created",
                schema=LogicSerializer
            ),
            400: "Bad Request"
        }
    )
    def post(self, request):
        data = request.data
        data['user'] = request.user.pk
        serializer = LogicSerializer(data=request.data)
        if serializer.is_valid():
            sensor_data = serializer.save()
            return Response(LogicSerializer(sensor_data).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
