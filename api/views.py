
from tareas.models import Preventa, User, Tareas
from tareas.asignacion_tareas import AsignacionTareas

#api
from api.serializer import PreventaSerializer
from rest_framework import viewsets
from rest_framework.response import Response


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

            nueva_preventa = Preventa.objects.create(preventa=data['preventa'],tipo_venta=data['tipo_venta'], tipo_cliente=data['tipo_cliente'],user=user)
            nueva_preventa.save()
            preventa = Preventa.objects.get(preventa = data['preventa'])
            if data['tipo_venta'] == 'Contado':
                AsignacionTareas.crear_tareas_preventa_contado(user,preventa)
            else:
                AsignacionTareas.crear_tareas_preventa_financiado(user,preventa)
            if data['tipo_cliente'] == "Persona Fisica":
                AsignacionTareas.crear_tareas_preventa_persona_fisica(user,preventa)
            else:
                AsignacionTareas.crear_tareas_preventa_persona_juridica(user,preventa)
            return Response(data)    

        except:
            return Response('no se creo la preventa')
    
