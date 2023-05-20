from django.contrib import admin

from greenhouse.base.v1.models.logicModel import LogicModel
from greenhouse.base.v1.models.masterModels import MasterModel
from greenhouse.base.v1.models.plantModels import PlantModel
from greenhouse.base.v1.models.slaveModels import SlaveModel

# Register your models here.
admin.site.register(PlantModel)
admin.site.register(MasterModel)
admin.site.register(SlaveModel)
admin.site.register(LogicModel)
