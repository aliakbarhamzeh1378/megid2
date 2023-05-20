from django.urls import path

from greenhouse.base.v1.views.logicView import LogicModelList, LogicModelDetail
from greenhouse.base.v1.views.masterView import MasterModelList, MasterModelDetail
from greenhouse.base.v1.views.plantView import PlantModelList, PlantModelDetail
from greenhouse.base.v1.views.slaveView import SlaveModelList, SlaveModelDetail

urlpatterns = [
    path('masters/', MasterModelList.as_view(), name='master-model-list'),
    path('masters/<int:pk>/', MasterModelDetail.as_view(), name='master-model-detail'),
    path('slaves/', SlaveModelList.as_view(), name='slave-model-list'),
    path('slaves/<int:pk>/', SlaveModelDetail.as_view(), name='slave-model-detail'),
    path('plants/', PlantModelList.as_view(), name='plant-model-list'),
    path('plants/<int:pk>/', PlantModelDetail.as_view(), name='plant-model-detail'),
    path('logic/', LogicModelList.as_view(), name='logic-model-list'),
    path('logic/<int:pk>/', LogicModelDetail.as_view(), name='logic-model-detail'),

]
