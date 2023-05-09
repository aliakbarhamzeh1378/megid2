from django.db import models


class PlantModel(models.Model):
    user_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100, null=False, blank=False)
    image = models.CharField(max_length=100, null=False, blank=False)
    temperature = models.FloatField(null=False, blank=False)
    light = models.FloatField(null=False, blank=False)
    moisture = models.CharField(max_length=100, null=False, blank=False)
    explanation = models.TextField(null=False, blank=False)

    def __str__(self):
        return str(self.name)
