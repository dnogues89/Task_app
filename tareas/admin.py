from django.contrib import admin
from .models import Tareas, Preventa, Vendedor, TipoTarea, AsignacionTareas, TipoDoc

class AsignacionTareasAdmin(admin.ModelAdmin):
    list_display = ('titulo','tipo','tipo_doc')
    list_filter = ('tipo',)
    raw_id_fields = ('tipo_doc',)
    autocomplete_fields = ('tipo_doc',)  # Esta línea habilita el autocompletado

    
class TipoDocAdmin(admin.ModelAdmin):
    search_fields = ('descripcion',)
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