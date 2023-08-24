
from tareas.models import Preventa, User, Tareas
from pagos.models import Pago
from tareas.asignacion_tareas import AsignacionTareas
from django.db.models import Q

#api
from api.serializer import PreventaSerializer, TareasSerializer, PagoSerializer
from rest_framework import viewsets

from django.http import Http404
from rest_framework.views import APIView

from rest_framework.response import Response


class TareasSerializerViewset(viewsets.ModelViewSet):
    queryset = Tareas.objects.all()
    serializer_class = TareasSerializer
    
    #Enviar al endpoint una preventa valida
    def list(self, requests):        
        # try:
        data = requests.data
        print(data)
        try:
            user = Preventa.objects.get(preventa=data['preventa'])
            preventa = user.id
            user = user.user_id
            queryset = Tareas.objects.filter(Q(user=user, pv=None) | Q(pv=preventa))
            print(queryset)
            serializer = TareasSerializer(queryset, many=True)
            print(serializer.data)
            return Response(serializer.data)
        except:
            serializer = TareasSerializer(self.queryset, many=True)
            return Response(serializer.data)
    


class PreventaSerializerViewSet(viewsets.ModelViewSet):
    queryset = Preventa.objects.all()
    serializer_class = PreventaSerializer   
        
    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            
            #Crear usuario si no existe
            try:
                user = User.objects.get(username=data['user'])
            except:
                user = User.objects.create(username = data['user'], password='abcd1234')
                user.set_password('abcd1234')
                user.save()
                AsignacionTareas.crear_tareas_usuario(user)

            nueva_preventa = Preventa.objects.create(preventa=data['preventa'],tipo_venta=data['tipo_venta'],user=user)
            nueva_preventa.save()
            preventa = Preventa.objects.get(preventa = data['preventa'])
            if data['tipo_venta'] == 'Contado':
                AsignacionTareas.crear_tareas_preventa_contado(user,preventa)
            else:
                AsignacionTareas.crear_tareas_preventa_financiado(user,preventa)
            return Response(data)    

        except:
            return Response('no se creo la preventa')
    

class PagoSerializerViewset(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    
    #Enviar al endpoint una preventa valida
    def list(self, requests):        
        data = requests.data
        try:
            preventa = Preventa.objects.get(preventa=data['preventa'])
            print(preventa)
            queryset = Pago.objects.filter(preventa= preventa)
            serializer = PagoSerializer(queryset, many=True)
            return Response(serializer.data)
        except:
            return Response("Preventa No valida")