from typing import Any, Dict, Tuple
from django.db import models
from django import forms
from tareas.models import Preventa
from django.utils import timezone
from django.utils.html import format_html
import os

def save_path(instance,filename):
    if instance.preventa is not None or instance.preventa != '':
        return f'pagos/{instance.preventa_id}/{filename}'
    return f'pagos/{filename}'


# Create your models here.
class Pago(models.Model):
    preventa = models.ForeignKey(Preventa, on_delete=models.CASCADE, blank=True, null=True)
    numero_comprobante = models.CharField(max_length=50)
    #choices =  #Opciones de pago a validar.
    #tipo de pago con las opciones.
    #Datos del depositante (cuil o cuit)
    depositante_cuit = models.IntegerField(verbose_name='Datos Depositante')
    monto = models.IntegerField()
    comprobante = models.ImageField(upload_to=save_path)
    motivo_rechazo = models.TextField(null=True,blank=True, max_length=1000)
    choices = [('1Pendiente','Pendiente'),('2Aprobado','Aprobado'),('3Rechazado','Rechazado')]
    estado = models.CharField(choices=choices, max_length=30, blank=True,default='1Pendiente')
    fecha_carga = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_aprobado = models.DateTimeField(blank=True, null=True)
    acreditado = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'{self.preventa} | ${self.monto}'
    
    def save(self, *args, **kwargs):
            try:
                self.comprobante.name = f'{self.numero_comprobante}.{self.comprobante.name.split(".")[-1]}'
                if self.pk is not None:   
                    # Obtener el objeto existente de la base de datos.
                    old_obj = Pago.objects.get(pk=self.pk)
                    # Verificar si el archivo adjunto ha sido modificado.
                    if old_obj.comprobante != self.comprobante:
                        # Eliminar el archivo adjunto anterior si ha sido modificado.
                        old_obj.comprobante.delete(save=False)
                        _,ext = os.path.splitext(os.path.basename(self.comprobante.name))
                        self.comprobante.name = f'{self.numero_comprobante}{ext}'
                        print(self.comprobante)
                        print(self.comprobante.name)
                    
                    
                    if self.estado == '2Aprobado':
                        if old_obj != None and old_obj.estado != '2Aprobado':
                            self.fecha_aprobado = timezone.now()
                    
                    if self.estado == '3Rechazado':
                        self.estado == '1Pendiente'
                    
            except:
                pass    
            # Guardar la instancia del modelo con el nuevo archivo adjunto.
            super().save(*args, **kwargs)
    
    def delete(self,*args,**kwargs):
        self.comprobante.delete()
        super().delete(*args,**kwargs)
    
    class Meta:
        verbose_name = 'pago'
        verbose_name_plural = 'pagos'
        
class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = '__all__'
        

class ImageWidget(forms.ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        if value:
            image_url = value.url
            preview = format_html('<br><img src="{}" style="max-height: 400px; max-width: auto;" />', image_url)
            return format_html('{}{}'.format(html, preview))
        return html


class PagoFormAdmin(forms.ModelForm):
    class Meta:
        model = Pago
        fields = '__all__'
        widgets = {
            'comprobante': ImageWidget(),
        }
    
    
    def preview_comprobante(self, instance):
        if instance.comprobante:
            return format_html('<img src="{}" width="200" height="200" />'.format(instance.comprobante.url))
        return ''
    
