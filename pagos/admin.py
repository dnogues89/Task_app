from django.contrib import admin
from django import forms


from pagos.models import Pago, PagoFormAdmin

# Register your models here.
class PagoAdmin(admin.ModelAdmin):
    list_display = ('preventa', 'numero_comprobante', 'precio_con_signo','administracion', 'estado','carga_crm','acreditado', 'fecha_carga', 'fecha_aprobado')
    search_fields = ('preventa', 'numero_comprobante', 'monto')
    list_filter = ['administracion','acreditado']
    date_hierarchy = 'fecha_carga'
    ordering = ['administracion','fecha_carga']
    exclude = ['fecha_aprobado',]

    form = PagoFormAdmin
    
    
    def precio_con_signo(self, obj):
        return "$ {:,.0f}".format(obj.monto).replace(",", ".")  # Formatea el precio con 2 decimales y separador de miles.
    precio_con_signo.short_description = 'Precio con Signo'

    

    
admin.site.register(Pago,PagoAdmin)