from django.db import models


class PermissionModel(models.Model):
    Title = models.CharField(max_length=100)
    Access = models.IntegerField(null=False,blank=False,unique=True)

    def __str__(self):
        return str(self.Title)
