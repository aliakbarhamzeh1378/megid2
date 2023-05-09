from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from greenhouse.base.v1.models.masterModels import MasterModel
from greenhouse.base.v1.serializers.masterSerializer import MasterModelSerializer


class MasterModelList(APIView):
    """
    List all master models or create a new one
    """

    @swagger_auto_schema(operation_summary="List all master models",
                         responses={200: MasterModelSerializer(many=True)})
    def get(self, request, format=None):
        master_models = MasterModel.objects.all()
        serializer = MasterModelSerializer(master_models, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_summary="Create a new master model",
                         request_body=MasterModelSerializer,
                         responses={201: MasterModelSerializer()})
    def post(self, request, format=None):
        serializer = MasterModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MasterModelDetail(APIView):
    """
    Retrieve, update or delete a master model instance
    """

    @swagger_auto_schema(operation_summary="Retrieve a specific master model",
                         responses={200: MasterModelSerializer()})
    def get(self, request, pk, format=None):
        master_model = self.get_object(pk)
        serializer = MasterModelSerializer(master_model)
        return Response(serializer.data)

    @swagger_auto_schema(operation_summary="Update a specific master model",
                         request_body=MasterModelSerializer,
                         responses={200: MasterModelSerializer()})
    def put(self, request, pk, format=None):
        master_model = self.get_object(pk)
        serializer = MasterModelSerializer(master_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Delete a specific master model",
                         responses={204: "No content"})
    def delete(self, request, pk, format=None):
        master_model = self.get_object(pk)
        master_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
