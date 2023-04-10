from django.db import models


class PermissionModel(models.Model):
    Title = models.CharField(max_length=100)

    def __str__(self):
        return str(self.Title)
