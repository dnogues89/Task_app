from django.urls import path, include
from .views import ListaTareas, DetalleTareas, CrearTarea, ActualizarTarea, EliminarTarea, MiLoginView, Registrarse, CrearPreventa,ListaPreventas, ListaTareasPreventa, ActualizarPreventa,download_file, MiPasswordResetView, MiPasswordResetDoneView, MiPasswordResetConfirmView, MiPasswordResetCompleteView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views




#media
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    #Vistas para el login
    path('login/', MiLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page = 'login'), name='logout'),
    path('registrarse/', Registrarse.as_view(),name='registrarse'),
    path(
        "password_change/", views.PasswordChangeView.as_view(), name="password_change"
    ),
    path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("password_reset/", MiPasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        MiPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        MiPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        MiPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),

    
    #Preventas Views
    path('crear-preventa',CrearPreventa.as_view(),name='crear-preventa'),
    path('preventas/',ListaPreventas.as_view(),name='preventas'),
    path('preventas/<int:pk>', ActualizarPreventa.as_view(),name='actualizar-preventa'),
    path('preventas/tareas/<int:pk>', ListaTareasPreventa.as_view(),name='lista-tareas-preventa'),
    
    #Tareas Views  
    path('',ListaTareas.as_view(),name='tareas'),
    path('tarea/<int:pk>/',DetalleTareas.as_view(),name='tarea'),
    path('crear-tarea/',CrearTarea.as_view(),name='crear-tarea'),
    path('actualizar-tarea/<int:pk>/',ActualizarTarea.as_view(),name='actualizar-tarea'),
    path('eliminar-tarea/<int:pk>/',EliminarTarea.as_view(),name='eliminar-tarea'),
    
    #descargar archivos
    path('download/<str:file_name>/', download_file, name='download_file'),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)