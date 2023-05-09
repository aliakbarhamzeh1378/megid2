from django.db import models

from greenhouse.base.v1.models.slaveModels import SlaveModel


class MasterModel(models.Model):
    name = models.CharField(max_length=100)
    slaves = models.ManyToManyField(SlaveModel, blank=True)

    def __str__(self):
        return str(self.name)
