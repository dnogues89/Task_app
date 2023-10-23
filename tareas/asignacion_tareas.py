from .models import Tareas, AsignacionTareas, TipoTarea, User

def crear_tarea(usuario,preventa,tipo):
    tipo_tarea = TipoTarea.objects.get(tipo=tipo)
    tareas = AsignacionTareas.objects.filter(tipo=tipo_tarea)
    for tarea in tareas:
        objeto = Tareas.objects.create(user = usuario, titulo = f'{tarea.titulo} | {preventa.preventa}', descripcion=tarea.descripcion, descarga=tarea.descarga, pv=preventa, tipo_doc = tarea.tipo_doc,tipo_tarea=tipo_tarea).save()
