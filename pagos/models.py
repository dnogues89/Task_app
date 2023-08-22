from django.db import models
from django import forms
from tareas.models import Preventa
import os

def save_path(instance,filename):
    if instance.preventa is not None or instance.preventa != '':
        return f'pagos/{instance.preventa_id}/{filename}'
    return f'pagos/{filename}'


# Create your models here.
class Pago(models.Model):
    preventa = models.ForeignKey(Preventa, on_delete=models.CASCADE, blank=True, null=True)
    numero_comprobante = models.IntegerField()
    #choices =  #Opciones de pago a validar.
    #tipo de pago con las opciones.
    #Datos del depositante (cuil o cuit)
    monto = models.IntegerField()
    comprobante = models.ImageField(upload_to=save_path)
    motivo_rechazo = models.TextField(null=True,blank=True, max_length=1000)
    choices = [('Pendiente','Pendiente'),('Aprobado','Aprobado'),('Rechazado','Rechazado')]
    estado = models.CharField(choices=choices, max_length=30, blank=True,auto_created='Pendiente')
    acreditado = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'{self.preventa} | ${self.monto}'
    
    def save(self, *args, **kwargs):
        try:
            # Verificar si se está modificando una instancia existente.
            if self.pk is not None:
                
                
                # Obtener el objeto existente de la base de datos.
                old_obj = Pago.objects.get(pk=self.pk)
                # Verificar si el archivo adjunto ha sido modificado.
                if old_obj.comprobante != self.comprobante:
                    # Eliminar el archivo adjunto anterior si ha sido modificado.
                    old_obj.comprobante.delete(save=False)
                    _,ext = os.path.splitext(os.path.basename(self.comprobante.name))
                    self.comprobante.name = f'{self.numero_comprobante}{ext}'
                    self.completo = True
        except:
            pass    
        # Guardar la instancia del modelo con el nuevo archivo adjunto.
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'pago'
        verbose_name_plural = 'pagos'
        
class PagoForm(forms.ModelForm):
    preventa = models.AutoField()
    
    class Meta:
        model = Pago
        fields = '__all__'
