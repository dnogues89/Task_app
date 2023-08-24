from django.contrib import admin
from django import forms

from pagos.models import Pago, PagoFormAdmin

# Register your models here.
class PagoAdmin(admin.ModelAdmin):
    list_display = ('preventa', 'numero_comprobante', 'monto', 'estado', 'fecha_carga', 'fecha_aprobado')
    search_fields = ('preventa', 'numero_comprobante', 'monto')
    date_hierarchy = 'fecha_carga'
    ordering = ['estado','fecha_carga']

    form = PagoFormAdmin
    
    
admin.site.register(Pago,PagoAdmin)