from django.contrib import admin
from .models import Tareas, Preventa, Vendedor, TipoTarea, AsignacionTareas, TipoDoc

class AsignacionTareasAdmin(admin.ModelAdmin):
    list_display = ('titulo','tipo')
    list_filter = ('tipo',)
    
class TipoDocAdmin(admin.ModelAdmin):
    list_display = ('tipo_id','descripcion')

class PreventaAdmin(admin.ModelAdmin):
    list_display = ('preventa','user_name','modelo',)
    
    def user_name(self, obj):
        try:
            return obj.user.first_name
        except:
            return obj.user

# Register your models here.
admin.site.register(Tareas)
admin.site.register(Preventa,PreventaAdmin)
admin.site.register(Vendedor)
admin.site.register(AsignacionTareas, AsignacionTareasAdmin)
admin.site.register(TipoTarea)
admin.site.register(TipoDoc,TipoDocAdmin)