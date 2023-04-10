from rest_framework import serializers

from api.base.v1.models.permisionsModel import PermissionModel
from api.base.v1.models.userModel import UserModel


class PermissionSerializer(serializers.ModelSerializer):
    Application = serializers.SlugRelatedField(
        # many=True,
        read_only=True,
        slug_field='Name'
    )
    class Meta:
        model = PermissionModel
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    DateJoin = serializers.DateTimeField(source='date_joined')
    LastLogin = serializers.DateTimeField(source='last_login')
    Permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = UserModel
        fields = ['Email', 'Username', 'DateJoin', 'LastLogin', 'pk', 'Permissions']
