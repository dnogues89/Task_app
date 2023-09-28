import requests
from django.http import JsonResponse
from tareas.models import Preventa, Tareas, User, TipoTarea, AsignacionTareas

from .models import CRMUpdates
from tareas import asignacion_tareas
from datetime import date

from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .key_espasa_api import espasa_key

def get_preventas(request,desde,hasta):
    cant_preventas = 0
    try:
        last_update = CRMUpdates.objects.get(tipo='get_preventas')
    except:
        last_update = CRMUpdates.objects.create(tipo='get_preventas', date=date.today())
        last_update.save()
    
    if desde != None:
        last_update.date = desde
        last_update.save()
        
    if last_update.date != date.today():

        url = f'https://gvcrmweb.backoffice.com.ar/apicrmespasa/v1/ventaokm/obtenerPreventas?fechaDesde={last_update.date}&fechaHasta={hasta}'
        
        last_update.date = date.today()
        last_update.save()
              
        
        headers = {"apiKey": espasa_key}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            for pv in data:
                if pv['tipoOperacion']== "Dealers":
                    cant_preventas+=1
                    try:
                        user = User.objects.get(username = pv['cliente']['cuit'].replace('-',''))
                        copiar_tareas_usuario = True
                    except:
                        copiar_tareas_usuario = False
                        user = User.objects.create(username = pv['cliente']['cuit'].replace('-',''), password='abcd1234')
                        user.set_password('abcd1234')
                        user.first_name = pv['cliente']['nombreCompleto']
                        user.save()
                        
                    
                    try:
                        nueva_preventa = Preventa.objects.get(preventa = pv['preventa'])
                    except:
                        nueva_preventa = Preventa.objects.create(preventa = pv['preventa'], user = user, fecha_preventa=pv['fecha'],modelo=pv['unidad']['descripcion'])
                        nueva_preventa.save()
                        if pv['tieneFinanciacion'] == "NO":
                            nueva_preventa.tipo_venta = 'Contado'
                            asignacion_tareas.crear_tarea(user,nueva_preventa,'preventa contado')
                        else:
                            nueva_preventa.tipo_venta = 'Financiado'
                            asignacion_tareas.crear_tarea(user,nueva_preventa,'preventa financiado')
                        nueva_preventa.save()
                    
                    if copiar_tareas_usuario:
                        tipo_tarea = TipoTarea.objects.get(tipo__icontains='tareas por usuario')
                        tareas_a_copiar = Tareas.objects.filter(user=user)
                        tareas_a_copiar = tareas_a_copiar.filter(tipo_tarea=tipo_tarea)
                        for tarea in tareas_a_copiar.values():
                            if tarea['completo']:
                                #cargar tarea en crm
                                
                                #chequear que se cargo
                                pass
                            else:
                                data = dict(tarea)
                                data.pop('id')
                                nueva_tarea = Tareas.objects.create(**data)
                                nueva_tarea.pv = nueva_preventa
                                nueva_tarea.save()
                                
                    else:
                        asignacion_tareas.crear_tarea(user,preventa=None,tipo='tareas por usuario')
                        if pv['cliente']['tipoPersona'] == 'Juridica':
                            asignacion_tareas.crear_tarea(user,preventa=None,tipo='tareas por usuario juridica')
                        
                        
    return JsonResponse({"Cantidad preventas importadas": cant_preventas})
            
@api_view(['GET'])
def enviar_tareas(request):
    tareas_queryset = Tareas.objects.filter(Q(completo=True) & Q(carga_crm=False))
    
    list_json = []
    for i in tareas_queryset:
        mi_dict = {'id':i.pk}
        try:
            mi_dict['preventa'] = i.pv.preventa
        except:
            mi_dict['preventa'] = None
        mi_dict['link'] = i.adjunto.url
        try:
            mi_dict['tipoAdjuntoID'] = i.tipo_doc.pk
        except:
            mi_dict['tipoAdjuntoID'] = None
        list_json.append(mi_dict)
        mi_dict['nombre']= i.titulo
        mi_dict['extension']=f".{str(i.adjunto.url).split('.')[-1]}"

        
    return JsonResponse({'':list_json})
    
    
