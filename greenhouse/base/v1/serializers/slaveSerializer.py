from rest_framework import serializers

from greenhouse.base.v1.models.slaveModels import SlaveModel


class SlaveModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlaveModel
        fields = '__all__'