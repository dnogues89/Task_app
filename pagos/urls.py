from django.urls import path
from pagos import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home,name='home'),
    #Vistas para el login
    path('preventas/',views.ListaPreventas.as_view(),name='pagos_preventa'),
    path('preventas/<int:pk>', views.ListaPagosPreventa.as_view(),name='lista-pagos-preventa'),
    path('preventas/pagos/<int:pk>', views.ActualizarPago.as_view(),name='actualizar-pago'),
    path('crear/', views.CrearPago.as_view(),name='crear-pago'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)