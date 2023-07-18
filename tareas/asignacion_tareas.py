from .models import Tareas
from django.utils.safestring import mark_safe

    # user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True)
    # titulo = models.CharField(max_length=200)
    # descripcion = models.TextField(null=True,blank=True)
    # adjunto = models.FileField(blank=True,null=True)
    # completo = models.BooleanField(default=False)
    # creado = models.DateField(auto_now_add=True)
    # pv = models.ForeignKey(Preventa, on_delete=models.SET_NULL, null=True,blank=True)


def crear_tareas_usuario(usuario):
    tarea = Tareas.objects.create(user = usuario, titulo = 'DNI Frente',descripcion='Foto frente dni del que firmo el boleto <a href="https://google.com.ar">LINK</a>')
    tarea.save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'DNI Dorso',descripcion='Foto dorso dni del que firmo el boleto')
    tarea.save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Constancia Cuit',descripcion='Constancia de CUIT de la reventa')
    tarea.save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Estatuto',descripcion='Estatuto completo en 1 archivo PDF')
    tarea.save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Ultima designacion de cargo',descripcion='Si no corresponde, marcar como completo')
    tarea.save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Constancia de CBU',descripcion='Imagen de constancia de CBU')
    tarea.save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Autorizacion Firmada',descripcion='Se necesita autorizacion en caso que la constancia de CBU no concuerde LINK DESCARGA')
    tarea.save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Cuentas Activas Firmadas',descripcion='Descargar, para firmar y subir archivo')
    tarea.save()