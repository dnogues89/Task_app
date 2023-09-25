
from rest_framework import serializers
from tareas.models import  Preventa, Tareas

class TareasSerializer(serializers.ModelSerializer):
    # Campos personalizados para seleccionar datos específicos de User y Preventa
    username = serializers.CharField(source='user.username')
    preventa = serializers.SerializerMethodField()
    modelo = serializers.SerializerMethodField()

    def get_preventa(self, obj):
        # Accede de manera segura al campo 'prevent'
        preventa_data = obj.pv
        if preventa_data:
            return preventa_data.preventa
        return None

    def get_modelo(self, obj):
        # Accede de manera segura al campo 'modelo'
        preventa_data = obj.pv
        if preventa_data:
            return preventa_data.modelo
        return None

    class Meta:
        model = Tareas
        fields = ['id', 'titulo', 'descripcion', 'adjunto', 'completo', 'actualizado', 'creado', 'carga_crm', 'username', 'modelo', 'preventa']



class PreventaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preventa
        fields = '__all__'
        depth = 1