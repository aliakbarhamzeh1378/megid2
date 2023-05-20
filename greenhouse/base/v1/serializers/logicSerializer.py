from rest_framework import serializers

from greenhouse.base.v1.models.logicModel import LogicModel


class LogicSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogicModel
        fields = '__all__'
