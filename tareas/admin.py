
from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import Tareas, Preventa, Vendedor, TipoTarea, AsignacionTareas, TipoDoc, Sucursal
from django.urls import reverse
from django.utils.html import format_html

class AsignacionTareasAdmin(admin.ModelAdmin):
    list_display = ('titulo','tipo','tipo_doc')
    list_filter = ('tipo',)
    raw_id_fields = ('tipo_doc',)
    search_fields = ('titulo',)
    autocomplete_fields = ('tipo_doc',)  # Esta línea habilita el autocompletado

class TareasAdmin(admin.ModelAdmin):
    list_display = ('titulo','pv_link','user_name','vendedor','sucursal','fecha','completo','carga_crm')
    ordering = ['creado','completo','carga_crm']
    list_filter = ['pv__vendedor','pv__vendedor__sucursal__sucursal','completo','carga_crm',]
    search_fields = ['pv__preventa','user__username','user__first_name']
    date_hierarchy = 'creado'
    exclude = ['crm_id','carga_crm','tipo_doc','pv','tipo_tarea','creado','descarga','completo','user']

    def pv_link(self, obj):
        if obj.pv:
            url = reverse('admin:tareas_preventa_change', args=[obj.pv.id])
            return format_html('<a href="{}">{}</a>', url, obj.pv)
        else:
            return "-"

    def vendedor(self,obj):
        try:
            return obj.pv.vendedor
        except:
            try:
                return Preventa.objects.get(user = obj.user).vendedor
            except:
                return '-'

    def sucursal(self,obj):
        try:
            return obj.pv.vendedor.sucursal
        except:
            try:
                return Preventa.objects.get(user = obj.user).vendedor.sucursal
            except:
                return '-'


    def fecha(self,obj):
        return obj.creado.strftime("%d/%m/%y") 
    
    
    def pv(self,obj):
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
            #supervisor
            is_supervisor = Sucursal.objects.get(supervisor = request.user)
            qs = qs.filter(pv__vendedor__sucursal=is_supervisor)
            for i in qs:
                qs = qs | Tareas.objects.filter(user = i.user)
            return qs
            
        except:
            try:
                #vendedor
                is_vendedor = Vendedor.objects.get(vendedor = request.user)
                qs = qs.filter(pv__vendedor=is_vendedor)
                for i in qs:
                    qs = qs | Tareas.objects.filter(user = i.user)
                return qs
            except:
                return qs
    


class TipoDocAdmin(admin.ModelAdmin):
    search_fields = ('descripcion',)
    list_display = ('tipo_id','descripcion')

class PreventaAdmin(admin.ModelAdmin):
    list_display = ('preventa','user_name','creado','modelo','vendedor','tareas_de_usuario_crm','pendientes', 'completo')
    date_hierarchy = 'fecha_preventa'
    search_fields = ['preventa']
    list_filter = ['vendedor','vendedor__sucursal']
    exclude = ['completo','tareas_de_usuario_crm','fecha_preventa','vendedor','contado','user']
    ordering = ('-fecha_preventa',)
    
    
    def creado(self,obj):
        return obj.fecha_preventa.strftime("%d/%m/%y") 
    
    def user_name(self, obj):
        try:
            return f'{obj.user.first_name[:15]}...' if len(obj.user.first_name) > 15 else obj.user.first_name
        except:
            return obj.user

    def pendientes(self, obj):
        try:
            tarea_count = Tareas.objects.filter(pv=obj).count()
            tareas = Tareas.objects.filter(pv=obj)
            url = reverse('admin:tareas_tareas_changelist') + f'?pv__id__exact={obj.id}'
            # return f'{tareas.count() - tareas.filter(completo=True).count()} / {tareas.count()}'
            return format_html(f'<a href="{url}">{tareas.count() - tareas.filter(completo=True).count()} / {tareas.count()}</a>')
        except:
            return 'Error rastreo'

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super().get_queryset(request)
        try:
            is_supervisor = Sucursal.objects.get(supervisor = request.user)
            qs = qs.filter(vendedor__sucursal=is_supervisor)
            return qs
        except:
            try:
                is_vendedor = Vendedor.objects.get(vendedor = request.user)
                qs = qs.filter(vendedor=is_vendedor)
                return qs
            except:
                return qs
            


class SucursalAdmin(admin.ModelAdmin):
    list_display = ('sucursal','gerente')
    
    def gerente(self,obj):
        return obj.supervisor.first_name
    
class VendedorAdmin(admin.ModelAdmin):
    list_display = ('nombre','sucursal','gerente')
    
    def nombre(self,obj):
        return obj.vendedor.first_name
    
    def gerente(self,obj):
        try:
            return obj.sucursal.supervisor.first_name
        except:
            return '-'

# Register your models here.
admin.site.register(Tareas,TareasAdmin)
admin.site.register(Preventa,PreventaAdmin)
admin.site.register(Vendedor,VendedorAdmin)
admin.site.register(AsignacionTareas, AsignacionTareasAdmin)
admin.site.register(TipoTarea)
admin.site.register(TipoDoc,TipoDocAdmin)
admin.site.register(Sucursal, SucursalAdmin)