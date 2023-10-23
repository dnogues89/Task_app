from .models import Tareas, AsignacionTareas, TipoTarea, User

def crear_tarea(usuario,preventa,tipo):
    tipo_tarea = TipoTarea.objects.get(tipo=tipo)
    tareas = AsignacionTareas.objects.filter(tipo=tipo_tarea)
    for tarea in tareas:
        if preventa != None:
            objeto = Tareas.objects.create(user = usuario, titulo = f'{preventa.preventa} | {tarea.titulo}', descripcion=tarea.descripcion, descarga=tarea.descarga, pv=preventa, tipo_doc = tarea.tipo_doc,tipo_tarea=tipo_tarea).save()
        else:            
            objeto = Tareas.objects.create(user = usuario, titulo = f'Tarea de Usuario | {tarea.titulo}', descripcion=tarea.descripcion, descarga=tarea.descarga, pv=preventa, tipo_doc = tarea.tipo_doc,tipo_tarea=tipo_tarea).save()
