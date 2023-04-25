from rest_framework import serializers

from api.base.v1.models.permisionsModel import PermissionModel
from api.base.v1.models.userModel import UserModel


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PermissionModel
        fields =['Access','Title']


class UserSerializer(serializers.ModelSerializer):
    DateJoin = serializers.DateTimeField(source='date_joined')
    LastLogin = serializers.DateTimeField(source='last_login')
    Permissions = PermissionSerializer(read_only=False)

    class Meta:
        model = UserModel
        fields = ['Email', 'Username', 'DateJoin', 'LastLogin', 'pk', 'Permissions','Slave_id']
