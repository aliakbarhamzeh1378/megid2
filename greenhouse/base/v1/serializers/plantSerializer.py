from rest_framework import serializers

from greenhouse.base.v1.models.plantModels import PlantModel


class PlantModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantModel
        fields = '__all__'