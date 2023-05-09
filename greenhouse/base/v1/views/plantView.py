from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from greenhouse.base.v1.models.plantModels import PlantModel
from greenhouse.base.v1.serializers.plantSerializer import PlantModelSerializer


class PlantModelList(APIView):
    """
    List all plant models or create a new one
    """

    @swagger_auto_schema(responses={200: PlantModelSerializer(many=True)})
    def get(self, request, format=None):
        plants = PlantModel.objects.all()
        serializer = PlantModelSerializer(plants, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=PlantModelSerializer, responses={201: PlantModelSerializer()})
    def post(self, request, format=None):
        serializer = PlantModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlantModelDetail(APIView):
    """
    Retrieve, update or delete a plant model instance
    """

    @swagger_auto_schema(responses={200: PlantModelSerializer()})
    def get(self, request, pk, format=None):
        plant = self.get_object(pk)
        serializer = PlantModelSerializer(plant)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=PlantModelSerializer, responses={200: PlantModelSerializer()})
    def put(self, request, pk, format=None):
        plant = self.get_object(pk)
        serializer = PlantModelSerializer(plant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk, format=None):
        plant = self.get_object(pk)
        plant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return PlantModel.objects.get(pk=pk)
        except PlantModel.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
