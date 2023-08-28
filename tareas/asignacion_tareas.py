from .models import Tareas, AsignacionTareas, TipoTarea, User

def crear_tareas_usuario(usuario):
    tipo_tarea = TipoTarea.objects.get(tipo='tareas por usuario')
    tareas = AsignacionTareas.objects.filter(tipo=tipo_tarea)
    for tarea in tareas:
        try:
            descarga = tarea.descarga.url
        except:
            descarga = ''
        objeto = Tareas.objects.create(user = usuario, titulo = tarea.titulo, descripcion=tarea.descripcion, descarga=tarea.descarga).save()

def crear_tareas_preventa_general(usuario,preventa):
    tarea = Tareas.objects.create(user = usuario, titulo = 'Titulo',descripcion='Adjuntar titulo NO CAT',pv=preventa,descarga='').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Patente',descripcion='Adjuntar patente',pv=preventa,descarga='').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Cedula Verde Frente',descripcion='Adjuntar Cedula Verde frente',pv=preventa,descarga='').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Cedula Verde Dorso',descripcion='Adjuntar Cedula Verde Dorso',pv=preventa,descarga='').save()

def crear_tarea_retira_cliente_final(usuario,preventa):
    tarea = Tareas.objects.create(user = usuario, titulo = 'Autorizacion retira titular',descripcion='Descargar archivo y adjuntar firmado', descarga="autorizacion", pv=preventa).save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Nota de turno',descripcion='Debe estar firmada por el titular. Archivo enviado por la administracion para firmar', pv=preventa).save()
    
def crear_tareas_retiro_individuo(usuario,preventa):
    tarea = Tareas.objects.create(user = usuario, titulo = 'DNI Frente retira unidad',descripcion='Foto frente dni del que retira',pv=preventa).save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'DNI Dorso retira unidad',descripcion='Foto dorso dni del que retira',pv=preventa).save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Autorizacion retira individup',descripcion='Descargar archivo y adjuntar firmado', pv=preventa).save()

def crear_tareas_retiro_transporte(usuario,preventa):
    tarea = Tareas.objects.create(user = usuario, titulo = 'Autorizacion empresa de transoporte',descripcion='Adjuntar autorizacion firmada en caso de retiro empresa de transporte',pv=preventa,descarga='').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Remito de transoporte',descripcion='Adjuntar remito en caso de retiro empresa de transporte',pv=preventa,descarga='').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'COT',descripcion='Adjuntar COT en caso de retiro empresa de transporte',pv=preventa,descarga='').save()

def crear_tareas_preventa_financiado(usuario,preventa):
    tarea = Tareas.objects.create(user = usuario, titulo = 'Credito Aprobado Firmado',descripcion='Descargar, para firmar y subir archivo (Titular de la prenda)',pv=preventa,descarga='Credito aprobado').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Anexo 1.2 del credito',descripcion='Descargar, para firmar y subir archivo (Titular de la prenda)',pv=preventa,descarga='ANEXO PARA OPERACIONES CON CRÉDITO PRENDARIO.pdf').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Prenda Inscripta',descripcion='Adjuntar prenda inscripta',pv=preventa,descarga='').save()


def crear_tareas_preventa_contado(usuario,preventa):
    tarea = Tareas.objects.create(user = usuario, titulo = 'Cuentas Activas Firmadas',descripcion='Descargar, para firmar y subir archivo',pv=preventa,descarga='').save()
    
def crear_tareas_preventa_persona_fisica(usuario,preventa):
    tarea = Tareas.objects.create(user = usuario, titulo = 'Titular DNI FRENTE',descripcion='Foto frente DNI titular',pv=preventa,descarga='').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Titular DNI DORSO',descripcion='Foto dorso DNI titular',pv=preventa,descarga='').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Titular Constancia de CUIL/CUIT',descripcion='Constancia de CUIT/CUIL Titular',pv=preventa,descarga='').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Pedido de refacturacion',descripcion='Descargar el archivo, debe firmar el mismo que firmo el boleto',pv=preventa, descarga='PEDIDO DE REFACTURACIÓN.pdf').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Nota Factura B',descripcion='Descargar el archivo, debe firmar el TITULAR. En caso que corresponda, sino marcar tarea como realizada.',pv=preventa, descarga='NOTA FACTURA B.doc').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Declaracion Jurada Persona Fisica',descripcion='Descargar el archivo, debe firmar y adjuntar',pv=preventa,descarga='DDJJ PERSONA FISICA 2023.doc').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Declaracion Jurada Persona Expuesta Politicamente',descripcion='Descargar el archivo, debe firmar y adjuntar. RECORDAR LA FIRMA EN AMBAS PAGINAS',pv=preventa,descarga='PEP 2023.doc').save()

def crear_tareas_preventa_persona_juridica(usuario,preventa):
    tarea = Tareas.objects.create(user = usuario, titulo = 'Estatuto',descripcion='Adjuntar 1 archivo completo',pv=preventa,descarga='').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Ultima designacion de cargo',descripcion='En caso que corresponda',pv=preventa,descarga='').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Inscripcion en la IGJ del ultimo domicilio legal',descripcion='Debe coincidir con la constancia de CUIT',pv=preventa,descarga='').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Declaracion Jurada Persona Juridica',descripcion='Descargar el archivo, debe firmar y adjuntar',pv=preventa,descarga='DDJJ PERSONA JURIDICA 2023.doc').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Declaracion Jurada Persona Expuesta Politicamente',descripcion='Descargar el archivo, debe firmar y adjuntar. RECORDAR LA FIRMA EN AMBAS PAGINAS',pv=preventa,descarga='PEP 2023.doc').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Certificacion Contable',descripcion='Adjuntar 1 solo archivo',pv=preventa).save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Guarda Habitual',descripcion='Se debe cargar si desea paatentar en un domicilio diferente',pv=preventa).save()

def crear_tarea_cotitulares(usuario,preventa):
    tarea = Tareas.objects.create(user = usuario, titulo = 'CO-Titular DNI FRENTE',descripcion='Foto frente DNI co-titular',pv=preventa,descarga='').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'CO-Titular DNI DORSO',descripcion='Foto dorso DNI co-titular',pv=preventa,descarga='').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'CO-Titular Constancia de CUIL/CUIT',descripcion='Constancia de CUIT/CUIL CO-Titular',pv=preventa,descarga='').save()
    
def crear_tarea_conyugue(usuario,preventa):
    tarea = Tareas.objects.create(user = usuario, titulo = 'Conyugue DNI FRENTE',descripcion='Foto frente DNI Conyugue',pv=preventa,descarga='').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Conyugue DNI DORSO',descripcion='Foto dorso DNI Conyugue',pv=preventa,descarga='').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Conyugue Constancia de CUIL/CUIT',descripcion='Conyugue de CUIT/CUIL',pv=preventa,descarga='').save()

def crear_cedula_azul(usuario,preventa):
    tarea = Tareas.objects.create(user = usuario, titulo = 'Cedula azul DNI FRENTE',descripcion='Foto frente DNI Cedula azul',pv=preventa,descarga='').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Cedula azul DNI DORSO',descripcion='Foto dorso DNI Cedula azul',pv=preventa,descarga='').save()

def crear_socio_persona_fisica(usuario,preventa):
    tarea = Tareas.objects.create(user = usuario, titulo = 'Socio DNI FRENTE',descripcion='Foto frente DNI Socio',pv=preventa,descarga='').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Socio DNI DORSO',descripcion='Foto dorso DNI Socio',pv=preventa,descarga='').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Declaracion Jurada Persona Fisica Socio',descripcion='Descargar el archivo, debe firmar y adjuntar (Socio para persona juridica)',pv=preventa,descarga='DDJJ PERSONA FISICA 2023.doc').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Declaracion Jurada Persona Expuesta Politicamente Socio',descripcion='Descargar el archivo, debe firmar y adjuntar (Socio para persona juridica). RECORDAR LA FIRMA EN AMBAS PAGINAS',pv=preventa,descarga='PEP 2023.doc').save()
    tarea = Tareas.objects.create(user = usuario, titulo = 'Socio Constancia de CUIL/CUIT',descripcion='Constancia de CUIT/CUIL Socio',pv=preventa,descarga='').save()
    
def crear_tarea(usuario,preventa,titulo,descripcion,descarga):
    tarea = Tareas.objects.create(user=usuario,preventa=preventa,titulo=titulo,descripcion=descripcion,descarga=descarga).save()
        
if '__main__' == __name__:
    user = User.objects.create(username = 'pruebisima', password='abcd1234')
    user.set_password('abcd1234')
    user.save()
    crear_tareas_usuario(user)