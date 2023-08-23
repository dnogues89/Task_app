from rest_framework import serializers
from tareas.models import  Preventa, Tareas
from pagos.models import Pago

class TareasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tareas
        fields = '__all__'
        depth = 1

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'
        depth = 1

class PreventaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preventa
        fields = '__all__'
        depth = 1
    
