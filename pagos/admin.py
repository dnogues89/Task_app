from django.contrib import admin
from django import forms


from pagos.models import Pago, PagoFormAdmin

# Register your models here.
class PagoAdmin(admin.ModelAdmin):
    list_display = ('preventa', 'numero_comprobante', 'monto','administracion', 'estado','carga_crm','acreditado', 'fecha_carga', 'fecha_aprobado')
    search_fields = ('preventa', 'numero_comprobante', 'monto')
    list_filter = ['administracion','acreditado']
    date_hierarchy = 'fecha_carga'
    ordering = ['administracion','fecha_carga']
    exclude = ['fecha_aprobado',]

    form = PagoFormAdmin
    

    
admin.site.register(Pago,PagoAdmin)