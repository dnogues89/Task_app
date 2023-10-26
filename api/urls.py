from django.urls import path

#media
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    #Vistas para el login
    path('get_preventas/', views.get_preventas, name='get-preventas-crm'),
    path('send_tareas/', views.enviar_tareas, name='send-tareas-crm'),
    #boletos
    path('get_boletos', views.get_boletos, name='get-boletos')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)