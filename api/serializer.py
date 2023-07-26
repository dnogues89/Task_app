from rest_framework import serializers
from tareas.models import  Preventa, Tareas

class TareasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tareas
        fields = '__all__'
        depth = 1

class PreventaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preventa
        fields = '__all__'
        depth = 1
    
