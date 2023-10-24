from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import Tareas, Preventa, Vendedor, TipoTarea, AsignacionTareas, TipoDoc

class AsignacionTareasAdmin(admin.ModelAdmin):
    list_display = ('titulo','tipo','tipo_doc')
    list_filter = ('tipo',)
    raw_id_fields = ('tipo_doc',)
    search_fields = ('titulo',)
    autocomplete_fields = ('tipo_doc',)  # Esta línea habilita el autocompletado

class TareasAdmin(admin.ModelAdmin):
    list_display = ('titulo','user','pv_preventa','user_name','completo','carga_crm',)
    ordering = ['completo','carga_crm']
    list_filter = ['completo','carga_crm']
    search_fields = ['pv__preventa',]

    def pv_preventa(self,obj):
        try:
            return obj.pv.preventa
        except:
            return obj.pv
    
    def user_name(self, obj):
        try:
            return obj.user.first_name
        except:
            return obj.user
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super().get_queryset(request)
        try:
            is_vendedor = Vendedor.objects.get(vendedor = request.user)
            qs = qs.filter(pv__vendedor=is_vendedor)
            return qs
        except:
            return qs


class TipoDocAdmin(admin.ModelAdmin):
    search_fields = ('descripcion',)
    list_display = ('tipo_id','descripcion')

class PreventaAdmin(admin.ModelAdmin):
    list_display = ('preventa','user_name','modelo','completo')
    date_hierarchy = 'fecha_inicio'
    search_fields = ['preventa','user__first_name','vendedor','completo']
    
    def user_name(self, obj):
        try:
            return obj.user.first_name
        except:
            return obj.user
        
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super().get_queryset(request)
        try:
            is_vendedor = Vendedor.objects.get(vendedor = request.user)
            qs = qs.filter(vendedor=is_vendedor)
            return qs
        except:
            return qs


# Register your models here.
admin.site.register(Tareas,TareasAdmin)
admin.site.register(Preventa,PreventaAdmin)
admin.site.register(Vendedor)
admin.site.register(AsignacionTareas, AsignacionTareasAdmin)
admin.site.register(TipoTarea)
admin.site.register(TipoDoc,TipoDocAdmin)