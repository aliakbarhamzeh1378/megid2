from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from greenhouse.base.v1.models.slaveModels import SlaveModel
from greenhouse.base.v1.serializers.slaveSerializer import SlaveModelSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SlaveModelList(APIView):
    """
    List all slave models or create a new one
    """

    @swagger_auto_schema(
        operation_description="Get all slave models",
        responses={
            200: openapi.Response(description="Success"),
            404: "Not Found"
        },
    )
    def get(self, request, format=None):
        slaves = SlaveModel.objects.all()
        serializer = SlaveModelSerializer(slaves, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new slave model",
        request_body=SlaveModelSerializer,
        responses={
            201: openapi.Response(description="Created"),
            400: "Bad Request"
        },
    )
    def post(self, request, format=None):
        serializer = SlaveModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SlaveModelDetail(APIView):
    """
    Retrieve, update or delete a slave model instance
    """

    @swagger_auto_schema(
        operation_description="Get a slave model",
        responses={
            200: openapi.Response(description="Success"),
            404: "Not Found"
        },
    )
    def get(self, request, pk, format=None):
        slave = self.get_object(pk)
        serializer = SlaveModelSerializer(slave)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a slave model",
        request_body=SlaveModelSerializer,
        responses={
            200: openapi.Response(description="Success"),
            400: "Bad Request",
            404: "Not Found"
        },
    )
    def put(self, request, pk, format=None):
        slave = self.get_object(pk)
        serializer = SlaveModelSerializer(slave, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a slave model",
        responses={
            204: openapi.Response(description="No Content"),
            404: "Not Found"
        },
    )
    def delete(self, request, pk, format=None):
        slave = self.get_object(pk)
        slave.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
