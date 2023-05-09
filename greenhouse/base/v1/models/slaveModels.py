from django.db import models

from greenhouse.base.v1.models.plantModels import PlantModel


class SlaveModel(models.Model):
    user = models.CharField(max_length=100)
    master_id = models.IntegerField(null=False, blank=False)
    slaveName = models.CharField(max_length=100, null=False, blank=False)
    plant = models.ForeignKey(PlantModel, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.slaveName)