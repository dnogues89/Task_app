from django.urls import path

#media
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    #Vistas para el login
    path('get_preventas/<str:desde>', views.get_preventas, name='get-preventas-crm'),
    path('send_tareas/', views.enviar_tareas, name='send-tareas-crm'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)