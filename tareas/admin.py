from django.contrib import admin
from .models import Tareas, Preventa, Vendedor, TipoTarea, AsignacionTareas

class AsignacionTareasAdmin(admin.ModelAdmin):
    list_display = ('tipo','titulo',)

# Register your models here.
admin.site.register(Tareas)
admin.site.register(Preventa)
admin.site.register(Vendedor)
admin.site.register(AsignacionTareas, AsignacionTareasAdmin)
admin.site.register(TipoTarea)