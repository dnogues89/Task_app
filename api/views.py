import requests
from django.http import JsonResponse
from tareas.models import Preventa, Tareas, User, TipoTarea, Vendedor

from .models import CRMUpdates, UploadErrors
from tareas import asignacion_tareas
from datetime import date

from django.db.models import Q

from rest_framework.decorators import api_view
from .key_espasa_api import espasa_key

import json

def app_user(data):

    try:
        user = User.objects.get(username = data['vendedor']['usuarioCRM'])
        vendedor = Vendedor.objects.get(vendedor = user)    
    except:
        user = User.objects.create(username = data['vendedor']['usuarioCRM'], first_name=data['vendedor']['nombre'], password='abcd1234')
        user.set_password('abcd1234')
        user.save()
        vendedor = Vendedor.objects.create(vendedor=user)
        vendedor.save()
        
        
    try:
        user = User.objects.get(username = data['cliente']['cuit'].replace('-',''))
        new_user = False
    except:
        new_user = True
        user = User.objects.create(username = data['cliente']['cuit'].replace('-',''), password='abcd1234')
        user.set_password('abcd1234')
        user.first_name = data['cliente']['nombreCompleto']
        user.email = data['cliente']['email']
        user.save()
        asignacion_tareas.crear_tarea(user,preventa=None,tipo='tareas por usuario')
        if data['cliente']['tipoPersona'] == 'Juridica':
            asignacion_tareas.crear_tarea(user,preventa=None,tipo='tareas por usuario juridica')
            
    return user, new_user, vendedor


def dealer_data(data):
    errores = False
    user , new_user, vendedor = app_user(data)
    nuevo_boleto = None
    try:
        boleto = Preventa.objects.get(preventa = data['preventa'])
    except:
        try:
            boleto = Preventa.objects.get(preventa = data['boleto'])
        except:
            nuevo_boleto = data['boleto']
            boleto = Preventa.objects.create(preventa = data['boleto'], user = user, fecha_preventa=data['fecha'],modelo=data['unidad']['descripcion'],vendedor=vendedor)
            boleto.save()
            
            if data['tieneFinanciacion'] == "NO":
                boleto.tipo_venta = 'Contado'
                asignacion_tareas.crear_tarea(user,boleto,'preventa contado')
            else:
                boleto.tipo_venta = 'Financiado'
                asignacion_tareas.crear_tarea(user,boleto,'preventa financiado')
            asignacion_tareas.crear_tarea(user,boleto,'boleto')
            boleto.save()
    
    if new_user == False:
        if boleto.tareas_de_usuario_crm == False:
            if Tareas.objects.filter(tipo_tarea__tipo__icontains = 'usuario').filter(user=user).filter(completo=False).count() == 0:
                tareas = Tareas.objects.filter(tipo_tarea__tipo__icontains = 'usuario').filter(user=user).filter(completo=True)
                for tarea in tareas:
                    mi_dict = tarea_to_json(tarea,'referencia')
                    mi_dict['referencia'] = boleto.preventa
                    crm = post_crm(mi_dict)
                    if crm[0]:
                        tarea.crm_id = crm[1]['idAdjunto']
                        tarea.carga_crm =True
                        tarea.save()
                    else:
                        error = UploadErrors.objects.create(tipo=mi_dict['nombre'],preventa=mi_dict['referencia'],log=f'ENVIADO:\n{mi_dict} \n\nRECIBIDO:\n{str(crm[1])}', date=date.today())
                        error.save()
                        error.save()
        
                boleto.tareas_de_usuario_crm = True
                boleto.save()

    return nuevo_boleto
            
def get_boletos(request):
    cant = 0
    importados = []
    url = f'https://gvcrmweb.backoffice.com.ar/apicrmespasa/v1/ventaokm/obtenerBoletos?fechaDesde=2023-10-01'
    headers = {"apiKey": espasa_key}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        for bol in data:
            if bol['tipoOperacion']== "Dealers":                
                boleto = dealer_data(bol)
                if boleto != None:
                    cant += 1
                    importados.append(boleto)
    
    return JsonResponse({"Cantidad": cant, 'Boletos':importados })
            
            
def get_preventas(request):
    get_boletos(request) 
    desde = '2023-10-24'
    cant_preventas = 0
    
    url = f'https://gvcrmweb.backoffice.com.ar/apicrmespasa/v1/ventaokm/obtenerPreventas?fechaDesde={desde}'
    
    headers = {"apiKey": espasa_key}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        for pv in data:
            if pv['tipoOperacion']== "Dealers": 
                try:
                    nueva_preventa = Preventa.objects.get(preventa = pv['preventa'])
                except:
                    try:
                        nueva_preventa = Preventa.objects.get(preventa = pv['boleto'])
                        
                        nueva_preventa.preventa = pv['preventa']
                        nueva_preventa.save()
                    except:
                        user , new_user, vendedor = app_user(data)
                        nueva_preventa = Preventa.objects.create(preventa = pv['preventa'], user = user, fecha_preventa=pv['fecha'],modelo=pv['unidad']['descripcion'], vendedor = vendedor)
                        nueva_preventa.save()
                       
    return JsonResponse({"Cantidad preventas importadas": cant_preventas})
            
@api_view(['GET'])
def enviar_tareas(request):
    tareas_queryset = Tareas.objects.filter(Q(completo=True) & Q(carga_crm=False))
    errores = []
    ok = []
    for i in tareas_queryset.exclude(pv=None):
        mi_dict = tarea_to_json(i,'preventa')
        crm = post_crm(mi_dict)
        if crm[0]:
            mi_dict['crm'] = crm[1]
            ok.append(mi_dict)
            i.carga_crm = True
            i.crm_id = crm[1]['idAdjunto']
            
        else:
            error = UploadErrors.objects.create(tipo=mi_dict['nombre'],preventa=i.pv.preventa,log=f'ENVIADO:\n{mi_dict} \n\nRECIBIDO:\n{str(crm[1])}', date=date.today())
            error.save()
            mi_dict['crm'] = crm[1]
            errores.append(mi_dict)
            i.crm_id = 'error de carga'
        i.save()

    return JsonResponse({'errores':errores,'ok':ok})

def tarea_to_json(tarea,tipo):
    if tarea.pv.preventa.split('-')[0] == "BE":
        tipo='referencia'
    else:
        tipo='preventa'
    mi_dict={}
    try:
        mi_dict[tipo] = tarea.pv.preventa
    except:
        mi_dict[tipo] = None
    mi_dict['link'] = f'https://espasadocu.com.ar{tarea.adjunto.url}'
    try:
        mi_dict['tipoAdjuntoID'] = tarea.tipo_doc.pk
    except:
        mi_dict['tipoAdjuntoID'] = None
    mi_dict['nombre']= tarea.titulo.split("|")[-1]
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