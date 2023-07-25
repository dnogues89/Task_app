from rest_framework import serializers
from tareas.models import  Preventa

class PreventaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preventa
        fields = '__all__'
        
    depth = 1
    
