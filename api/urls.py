from django.urls import path

#media
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    #Vistas para el login
    path('preventas/', views.get_preventas, name='get-preventas'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)