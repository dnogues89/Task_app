from django.urls import path,include
from rest_framework import routers

from .views import PreventaSerializerViewSet, TareasSerializerViewset,PagoSerializerViewset

routers = routers.DefaultRouter()
routers.register(r'preventas',PreventaSerializerViewSet)
routers.register(r'tareas',TareasSerializerViewset)
routers.register(r'pagos',PagoSerializerViewset)

urlpatterns = [
    #Api
    path('', include(routers.urls))
    
]