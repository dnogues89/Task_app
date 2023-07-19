from .models import Tareas
from django.utils.safestring import mark_safe

    # user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True)
    # titulo = models.CharField(max_length=200)
    # descripcion = models.TextField(null=True,blank=True)
    # adjunto = models.FileField(blank=True,null=True)
    # completo = models.BooleanField(default=False)
    # creado = models.DateField(auto_now_add=True)
    # pv = models.ForeignKey(Preventa, on_delete=models.SET_NULL, null=True,blank=True)

class AsignacionTareas():

    def crear_tareas_usuario(usuario):
        tarea = Tareas.objects.create(user = usuario, titulo = 'DNI Frente',descripcion='Foto frente dni del que firmo el boleto', descarga="https://google.com.ar")
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

    def crear_tareas_preventa_general(usuario,preventa):
        tarea = Tareas.objects.create(user = usuario, titulo = 'Titulo',descripcion='Adjuntar titulo NO CAT',pv=preventa,descarga='')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'Patente',descripcion='Adjuntar patente',pv=preventa,descarga='')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'Cedula Verde Frente',descripcion='Adjuntar Cedula Verde frente',pv=preventa,descarga='')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'Cedula Verde Dorso',descripcion='Adjuntar Cedula Verde Dorso',pv=preventa,descarga='')
        tarea.save()

    def crear_tarea_retira_cliente_final(usuario,preventa):
        tarea = Tareas.objects.create(user = usuario, titulo = 'Autorizacion retira titular',descripcion='Descargar archivo y adjuntar firmado', descarga="autorizacion", pv=preventa)
        tarea.save()
        
    def crear_tareas_retiro_individuo(usuario,preventa):
        tarea = Tareas.objects.create(user = usuario, titulo = 'DNI Frente',descripcion='Foto frente dni del que retira', descarga="https://google.com.ar",pv=preventa)
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'DNI Dorso',descripcion='Foto dorso dni del que retira',pv=preventa)
        tarea.save()

    def crear_tareas_retiro_transporte(usuario,preventa):
        tarea = Tareas.objects.create(user = usuario, titulo = 'Autorizacion empresa de transoporte',descripcion='Adjuntar autorizacion firmada en caso de retiro empresa de transporte',pv=preventa,descarga='')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'Remito de transoporte',descripcion='Adjuntar remito en caso de retiro empresa de transporte',pv=preventa,descarga='')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'COT',descripcion='Adjuntar COT en caso de retiro empresa de transporte',pv=preventa,descarga='')
        tarea.save()

    def crear_tareas_preventa_financiado(usuario,preventa):
        tarea = Tareas.objects.create(user = usuario, titulo = 'Credito Aprobado Firmado',descripcion='Descargar, para firmar y subir archivo (Titular de la prenda)',pv=preventa,descarga='Credito aprobado')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'Anexo 1.2 del credito',descripcion='Descargar, para firmar y subir archivo (Titular de la prenda)',pv=preventa,descarga='Anexo 1.2')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'Prenda Inscripta',descripcion='Adjuntar prenda inscripta',pv=preventa,descarga='')
        tarea.save()


    def crear_tareas_preventa_contado(usuario,preventa):
        tarea = Tareas.objects.create(user = usuario, titulo = 'Cuentas Activas Firmadas',descripcion='Descargar, para firmar y subir archivo',pv=preventa,descarga='')
        tarea.save()
        
    def crear_tareas_preventa_persona_fisica(usuario,preventa):
        tarea = Tareas.objects.create(user = usuario, titulo = 'Titular DNI FRENTE',descripcion='Foto frente DNI titular',pv=preventa,descarga='')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'Titular DNI DORSO',descripcion='Foto dorso DNI titular',pv=preventa,descarga='')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'Titular Constancia de CUIL/CUIT',descripcion='Constancia de CUIT/CUIL Titular',pv=preventa,descarga='')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'Pedido de refacturacion',descripcion='Descargar el archivo, debe firmar el mismo que firmo el boleto',pv=preventa,descarga='archivo')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'Declaracion Jurada Persona Fisica',descripcion='Descargar el archivo, debe firmar y adjuntar',pv=preventa,descarga='ddj fisica')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'Declaracion Jurada Persona Expuesta Politicamente',descripcion='Descargar el archivo, debe firmar y adjuntar',pv=preventa,descarga='ddj PEP')
        tarea.save()

    def crear_tareas_preventa_persona_juridica(usuario,preventa):
        tarea = Tareas.objects.create(user = usuario, titulo = 'Estatuto',descripcion='Adjuntar 1 archivo completo',pv=preventa,descarga='')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'Ultima designacion de cargo',descripcion='En caso que corresponda',pv=preventa,descarga='')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'Inscripcion en la IGJ del ultimo domicilio legal',descripcion='Debe coincidir con la constancia de CUIT',pv=preventa,descarga='')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'Declaracion Jurada Persona Juridica',descripcion='Descargar el archivo, debe firmar y adjuntar',pv=preventa,descarga='ddj juridica')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'Declaracion Jurada Persona Expuesta Politicamente',descripcion='Descargar el archivo, debe firmar y adjuntar',pv=preventa,descarga='ddj PEP')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'Certificacion Contable',descripcion='Adjuntar 1 solo archivo',pv=preventa,descarga='ddj PEP')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'Guarda Habitual',descripcion='Se debe cargar si desea paatentar en un domicilio diferente',pv=preventa,descarga='ddj PEP')
        tarea.save()

    def crear_tarea_cotitulares(usuario,preventa):
        tarea = Tareas.objects.create(user = usuario, titulo = 'CO-Titular DNI FRENTE',descripcion='Foto frente DNI co-titular',pv=preventa,descarga='')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'CO-Titular DNI DORSO',descripcion='Foto dorso DNI co-titular',pv=preventa,descarga='')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'CO-Titular Constancia de CUIL/CUIT',descripcion='Constancia de CUIT/CUIL CO-Titular',pv=preventa,descarga='')
        tarea.save()
        
    def crear_tarea_conyugue(usuario,preventa):
        tarea = Tareas.objects.create(user = usuario, titulo = 'Conyugue DNI FRENTE',descripcion='Foto frente DNI Conyugue',pv=preventa,descarga='')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'Conyugue DNI DORSO',descripcion='Foto dorso DNI Conyugue',pv=preventa,descarga='')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'Conyugue Constancia de CUIL/CUIT',descripcion='Conyugue de CUIT/CUIL',pv=preventa,descarga='')
        tarea.save()

    def crear_cedula_azul(usuario,preventa):
        tarea = Tareas.objects.create(user = usuario, titulo = 'Cedula azul DNI FRENTE',descripcion='Foto frente DNI Cedula azul',pv=preventa,descarga='')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'Cedula azul DNI DORSO',descripcion='Foto dorso DNI Cedula azul',pv=preventa,descarga='')
        tarea.save()

    def crear_socio_persona_fisica(usuario,preventa):
        tarea = Tareas.objects.create(user = usuario, titulo = 'Socio DNI FRENTE',descripcion='Foto frente DNI Socio',pv=preventa,descarga='')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'Socio DNI DORSO',descripcion='Foto dorso DNI Socio',pv=preventa,descarga='')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'Declaracion Jurada Persona Fisica Socio',descripcion='Descargar el archivo, debe firmar y adjuntar (Socio para persona juridica)',pv=preventa,descarga='ddj fisica')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'Declaracion Jurada Persona Expuesta Politicamente Socio',descripcion='Descargar el archivo, debe firmar y adjuntar (Socio para persona juridica)',pv=preventa,descarga='ddj PEP')
        tarea.save()
        tarea = Tareas.objects.create(user = usuario, titulo = 'Socio Constancia de CUIL/CUIT',descripcion='Constancia de CUIT/CUIL Socio',pv=preventa,descarga='')
        tarea.save()