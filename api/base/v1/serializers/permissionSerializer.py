from rest_framework import serializers

from api.base.v1.models.permisionsModel import PermissionModel
from api.base.v1.models.userModel import UserModel


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionModel
        fields = '__all__'
