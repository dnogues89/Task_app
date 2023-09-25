import requests
from django.http import JsonResponse
from tareas.models import Preventa, Tareas, User

from .models import CRMUpdates
from tareas import asignacion_tareas
from datetime import date

from django.core import serializers
from django.db.models import Q

from rest_framework.decorators import api_view
from .serializer import TareasSerializer
from rest_framework.response import Response
from .key_espasa_api import espasa_key


def get_preventas(request):
    cant_preventas = 0
    try:
        last_update = CRMUpdates.objects.get(tipo='get_preventas')
        print(last_update)
    except:
        last_update = CRMUpdates.objects.create(tipo='get_preventas', date=date.today())
        last_update.save()
        
    if last_update.date != date.today():
        last_update.date = date.today()
        last_update.save()
        url = f'https://gvcrmweb.backoffice.com.ar/apicrmespasa/v1/ventaokm/obtenerPreventas?fechaDesde={last_update.date}'
        
        headers = {"apiKey": espasa_key}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            for pv in data:
                if pv['tipoOperacion']== "Dealers":
                    cant_preventas+=1
                    try:
                        user = User.objects.get(username = pv['cliente']['cuit'].replace('-',''))
                    except:
                        user = User.objects.create(username = pv['cliente']['cuit'].replace('-',''), password='abcd1234')
                        user.set_password('abcd1234')
                        user.first_name = pv['cliente']['nombreCompleto']
                        user.save()
                        asignacion_tareas.crear_tareas_usuario(user)
                    
                    try:
                        preventa = Preventa.objects.get(preventa = pv['preventa'])
                    except:
                        nueva_preventa = Preventa.objects.create(preventa = pv['preventa'], user = user, fecha_preventa=pv['fecha'],modelo=pv['unidad']['descripcion'])
                        nueva_preventa.save()
                        if pv['tieneFinanciacion'] == "NO":
                            nueva_preventa.tipo_venta = 'Contado'
                            asignacion_tareas.crear_tareas_preventa_contado(user,nueva_preventa)
                        else:
                            nueva_preventa.tipo_venta = 'Financiado'
                            asignacion_tareas.crear_tareas_preventa_financiado(user,nueva_preventa)
                        nueva_preventa.save()
                        
    return JsonResponse({"Cantidad preventas importadas": cant_preventas})
            
@api_view(['GET'])
def enviar_tareas(request):
    import json
    tareas_queryset = Tareas.objects.filter(Q(completo=True) & Q(carga_crm=False))
    tareas_serializadas = TareasSerializer(tareas_queryset, many=True)

    return Response(tareas_serializadas.data)
    
    
