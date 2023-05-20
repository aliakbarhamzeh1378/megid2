from django.db import models

from api.base.v1.models.userModel import UserModel


class LogicModel(models.Model):
    sensor_name = models.CharField(max_length=255)
    data_json = models.JSONField()
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.sensor_name
