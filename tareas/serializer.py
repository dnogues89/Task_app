from rest_framework import serializers
from .models import Tareas, Preventa, User

class PreventaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preventa
        fields = '__all__'
        
    