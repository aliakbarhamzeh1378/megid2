from rest_framework import serializers

from greenhouse.base.v1.models.masterModels import MasterModel


class MasterModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterModel
        fields = '__all__'
