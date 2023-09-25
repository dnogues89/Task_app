from .models import Tareas, AsignacionTareas, TipoTarea, User

def crear_tareas_usuario(usuario):
    tipo_tarea = TipoTarea.objects.get(tipo='tareas por usuario')
    tareas = AsignacionTareas.objects.filter(tipo=tipo_tarea)
    for tarea in tareas:
        objeto = Tareas.objects.create(user = usuario, titulo = tarea.titulo, descripcion=tarea.descripcion, descarga=tarea.descarga, tipo_doc = tarea.tipo_doc).save()

def crear_tareas_preventa_general(usuario,preventa):
    tipo_tarea = TipoTarea.objects.get(tipo='preventa general')
    tareas = AsignacionTareas.objects.filter(tipo=tipo_tarea)
    for tarea in tareas:
        objeto = Tareas.objects.create(user = usuario, titulo = tarea.titulo, descripcion=tarea.descripcion, descarga=tarea.descarga, pv=preventa, tipo_doc = tarea.tipo_doc).save()


def crear_tarea_retira_cliente_final(usuario,preventa):
    tipo_tarea = TipoTarea.objects.get(tipo='retira cliente final')
    tareas = AsignacionTareas.objects.filter(tipo=tipo_tarea)
    for tarea in tareas:
        objeto = Tareas.objects.create(user = usuario, titulo = tarea.titulo, descripcion=tarea.descripcion, descarga=tarea.descarga, pv=preventa, tipo_doc = tarea.tipo_doc).save()
    
    
def crear_tareas_retiro_individuo(usuario,preventa):
    tipo_tarea = TipoTarea.objects.get(tipo='retira individuo')
    tareas = AsignacionTareas.objects.filter(tipo=tipo_tarea)
    for tarea in tareas:
        objeto = Tareas.objects.create(user = usuario, titulo = tarea.titulo, descripcion=tarea.descripcion, descarga=tarea.descarga, pv=preventa, tipo_doc = tarea.tipo_doc).save()

def crear_tareas_retiro_transporte(usuario,preventa):
    tipo_tarea = TipoTarea.objects.get(tipo='retira transporte')
    tareas = AsignacionTareas.objects.filter(tipo=tipo_tarea)
    for tarea in tareas:
        objeto = Tareas.objects.create(user = usuario, titulo = tarea.titulo, descripcion=tarea.descripcion, descarga=tarea.descarga, pv=preventa, tipo_doc = tarea.tipo_doc).save()

def crear_tareas_preventa_financiado(usuario,preventa):
    tipo_tarea = TipoTarea.objects.get(tipo='preventa financiado')
    tareas = AsignacionTareas.objects.filter(tipo=tipo_tarea)
    for tarea in tareas:
        objeto = Tareas.objects.create(user = usuario, titulo = tarea.titulo, descripcion=tarea.descripcion, descarga=tarea.descarga, pv=preventa, tipo_doc = tarea.tipo_doc).save()

def crear_tareas_preventa_contado(usuario,preventa):
    tipo_tarea = TipoTarea.objects.get(tipo='preventa contado')
    tareas = AsignacionTareas.objects.filter(tipo=tipo_tarea)
    for tarea in tareas:
        objeto = Tareas.objects.create(user = usuario, titulo = tarea.titulo, descripcion=tarea.descripcion, descarga=tarea.descarga, pv=preventa, tipo_doc = tarea.tipo_doc).save()

def crear_tareas_preventa_persona_fisica(usuario,preventa):
    tipo_tarea = TipoTarea.objects.get(tipo='persona fisica')
    tareas = AsignacionTareas.objects.filter(tipo=tipo_tarea)
    for tarea in tareas:
        objeto = Tareas.objects.create(user = usuario, titulo = tarea.titulo, descripcion=tarea.descripcion, descarga=tarea.descarga, pv=preventa, tipo_doc = tarea.tipo_doc).save()

def crear_tareas_preventa_persona_juridica(usuario,preventa):
    tipo_tarea = TipoTarea.objects.get(tipo='persona juridica')
    tareas = AsignacionTareas.objects.filter(tipo=tipo_tarea)
    for tarea in tareas:
        objeto = Tareas.objects.create(user = usuario, titulo = tarea.titulo, descripcion=tarea.descripcion, descarga=tarea.descarga, pv=preventa, tipo_doc = tarea.tipo_doc).save()
        
def crear_tarea_cotitulares(usuario,preventa):
    tipo_tarea = TipoTarea.objects.get(tipo='cotitulares')
    tareas = AsignacionTareas.objects.filter(tipo=tipo_tarea)
    for tarea in tareas:
        objeto = Tareas.objects.create(user = usuario, titulo = tarea.titulo, descripcion=tarea.descripcion, descarga=tarea.descarga, pv=preventa, tipo_doc = tarea.tipo_doc).save()


def crear_tarea_conyugue(usuario,preventa):
    tipo_tarea = TipoTarea.objects.get(tipo='conyuge')
    tareas = AsignacionTareas.objects.filter(tipo=tipo_tarea)
    for tarea in tareas:
        objeto = Tareas.objects.create(user = usuario, titulo = tarea.titulo, descripcion=tarea.descripcion, descarga=tarea.descarga, pv=preventa, tipo_doc = tarea.tipo_doc).save()


def crear_cedula_azul(usuario,preventa):
    tipo_tarea = TipoTarea.objects.get(tipo='cedula azul')
    tareas = AsignacionTareas.objects.filter(tipo=tipo_tarea)
    for tarea in tareas:
        objeto = Tareas.objects.create(user = usuario, titulo = tarea.titulo, descripcion=tarea.descripcion, descarga=tarea.descarga, pv=preventa, tipo_doc = tarea.tipo_doc).save()

def crear_socio_persona_fisica(usuario,preventa):
    tipo_tarea = TipoTarea.objects.get(tipo='socio persona fisica')
    tareas = AsignacionTareas.objects.filter(tipo=tipo_tarea)
    for tarea in tareas:
        objeto = Tareas.objects.create(user = usuario, titulo = tarea.titulo, descripcion=tarea.descripcion, descarga=tarea.descarga, pv=preventa, tipo_doc = tarea.tipo_doc).save()
        
def crear_tarea(usuario,preventa,titulo,descripcion,descarga):
    tarea = Tareas.objects.create(user=usuario,preventa=preventa,titulo=titulo,descripcion=descripcion,descarga=descarga, tipo_doc = tarea.tipo_doc).save()
        
if '__main__' == __name__:
    user = User.objects.create(username = 'pruebisima', password='abcd1234')
    user.set_password('abcd1234')
    user.save()
    crear_tareas_usuario(user)