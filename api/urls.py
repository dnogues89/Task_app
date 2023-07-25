from django.urls import path,include
from rest_framework import routers

from .views import PreventaSerializerViewSet

routers = routers.DefaultRouter()
routers.register(r'preventas',PreventaSerializerViewSet)

urlpatterns = [
    #Api
    path('', include(routers.urls))
    
]