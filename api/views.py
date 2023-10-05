import requests
from django.http import JsonResponse
from tareas.models import Preventa, Tareas, User, TipoTarea

from .models import CRMUpdates
from tareas import asignacion_tareas
from datetime import date

from django.db.models import Q

from rest_framework.decorators import api_view
from .key_espasa_api import espasa_key

import json

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
                        tipo_tarea = TipoTarea.objects.get(tipo='tareas por usuario')
                        tareas_a_copiar = Tareas.objects.filter(user=user)
                        tareas_a_copiar = tareas_a_copiar.filter(tipo_tarea=tipo_tarea)
                        for tarea in tareas_a_copiar:
                            if tarea.completo:
                                #cargar tarea en crm
                                mi_dict = tarea_to_json(tarea)
                                crm = post_crm(mi_dict)
                                if crm[0]:
                                    mi_dict['crm'] = crm[1]
                                else:
                                    mi_dict['crm'] = crm[1]
                    else:
                        asignacion_tareas.crear_tarea(user,preventa=None,tipo='tareas por usuario')
                        if pv['cliente']['tipoPersona'] == 'Juridica':
                            asignacion_tareas.crear_tarea(user,preventa=None,tipo='tareas por usuario juridica')
                        
                        
    return JsonResponse({"Cantidad preventas importadas": cant_preventas})
            
@api_view(['GET'])
def enviar_tareas(request):
    tareas_queryset = Tareas.objects.filter(Q(completo=True) & Q(carga_crm=False))
    errores = []
    ok = []
    for i in tareas_queryset:
        mi_dict = tarea_to_json(i)
        crm = post_crm(mi_dict)
        if crm[0]:
            mi_dict['crm'] = crm[1]
            ok.append(mi_dict)
            i.carga_crm = True
            i.crm_id = crm[1]['idAdjunto']
            
        else:
            mi_dict['crm'] = crm[1]
            errores.append(mi_dict)
            i.crm_id = 'error de carga'
        i.save()

    return JsonResponse({'errores':errores,'ok':ok})

def tarea_to_json(tarea):
    mi_dict={}
    try:
        mi_dict['preventa'] = tarea.pv.preventa
    except:
        mi_dict['preventa'] = None
    mi_dict['link'] = f'https://espasadocu.com.ar{tarea.adjunto.url}'
    try:
        mi_dict['tipoAdjuntoID'] = tarea.tipo_doc.pk
    except:
        mi_dict['tipoAdjuntoID'] = None
    mi_dict['nombre']= tarea.titulo
    mi_dict['extension']=f".{str(tarea.adjunto.url).split('.')[-1]}"
    
    return mi_dict
        

def post_crm(data):
    url = f'https://gvcrmweb.backoffice.com.ar/apicrmespasa/v1/ventaokm/altaAdjuntoPreventa'
    headers = {"apiKey": espasa_key, 'Content-Type': 'application/json'}
    
    json_data = json.dumps(data)
    response = requests.post(url, data=json_data, headers=headers)

    
    if response.status_code == 200:
        return True, response.json()
    else:
        return False, response.json()