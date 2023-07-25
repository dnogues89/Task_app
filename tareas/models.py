from typing import Any, Dict, Iterable, Optional, Tuple
import os
from django.db import models
from django import forms
from django.contrib.auth.models import User

def save_path(instance,filename):
    if instance.pv is not None or instance.pv != '':
        return f'user_{instance.user.id}/{instance.pv_id}/{filename}'
    return f'user_{instance.user.id}/{filename}'

# Create your models here.
class Vendedor(models.Model):
    vendedor=models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.vendedor.username
    
    class Meta:
        verbose_name = 'vendedor'
        verbose_name_plural = 'vendedores'
        


class Preventa(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True)
    preventa = models.CharField(max_length=8, help_text="Ejemplo 12345/1",unique=True)
    choises = [('Contado','Contado'),('Financiado','Financiado')]
    tipo_venta = models.CharField(max_length= 15, choices=choises)
    choises = [('Persona Fisica','Persona Fisica'),('Persona Juridica','Persona Juridica')]
    tipo_cliente = models.CharField(max_length=30,choices=choises)
    choises = [('Transportista','Transportista'),('Individuo','Individuo'),('Titular','Titular')]
    retira_unidad = models.CharField(max_length= 15, choices=choises, blank=True,null=True)
    cedulas_azules = models.IntegerField(blank=True,null=True)
    socios = models.IntegerField(blank=True,null=True)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, null=True,blank=True)
    completo=models.BooleanField(default=False)
    fecha_inicio = models.DateTimeField(auto_now=True,verbose_name='Fecha de creacion')
    


    
    def __str__(self) -> str:
        return self.preventa

class PreventaForm(forms.ModelForm):
    user = forms.ModelChoiceField(required=False,queryset=User.objects.all(), disabled=True,label="Usuario")
    preventa = forms.CharField(required=False,disabled=True,label='Numero de Preventa')
    tipo_cliente = forms.CharField(required=False, disabled=True, label='Tipo de cliente final')
    choises = [('',''),('Transportista','Transportista'),('Individuo','Individuo'),('Titular','Titular')]
    retira_unidad = forms.ChoiceField(choices= choises, required=False, disabled=False, label='Quien retira la unidad?')
    cedulas_azules = forms.IntegerField(required=False, label='Cantidad cedulas azules. En numero')
    socios = forms.IntegerField(required=False,label='Si es persona Juridica debe indicar cuantos socios. En numero')
    vendedor = forms.ModelChoiceField(required=False,queryset=Vendedor.objects.all(), disabled=True)
    completo = forms.BooleanField(required=False, label='Operacion terminada.')

    
    
    
    class Meta:
        model = Preventa
        fields = '__all__'
    
    
class Tareas(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(null=True,blank=True)
    descarga = models.URLField(null=True,blank=True)
    adjunto = models.FileField(blank=True,null=True,upload_to=save_path)
    completo = models.BooleanField(default=False)
    # actualizado = models.DateField(auto_created=) # fecha de actualizacion para 
    creado = models.DateField(auto_now_add=True)
    pv = models.ForeignKey(Preventa, on_delete=models.CASCADE, null=True,blank=True)
    
    def __str__(self) -> str:
        return self.titulo
    
    def save(self, *args, **kwargs):
        # Verificar si se está modificando una instancia existente.
        if self.pk is not None:
            try:
                # Obtener el objeto existente de la base de datos.
                old_obj = Tareas.objects.get(pk=self.pk)

            except Tareas.DoesNotExist:
                pass
            else:
                # Verificar si el archivo adjunto ha sido modificado.
                if old_obj.adjunto != self.adjunto:
                    # Eliminar el archivo adjunto anterior si ha sido modificado.
                    old_obj.adjunto.delete(save=False)
                    #Nombre del archivo
            
            try:
                #nombre de archivo
                _,ext = os.path.splitext(os.path.basename(self.adjunto.name))
                self.adjunto.name = f'{self.titulo}{ext}'
            except:
                pass
        
        # Guardar la instancia del modelo con el nuevo archivo adjunto.
        super().save(*args, **kwargs)

    
    def delete(self, using: Any = None, keep_parents: bool = False) -> Tuple[int, Dict[str, int]]:
        self.adjunto.delete()
        super().delete(using=using, keep_parents=keep_parents)
        

    
    
    class Meta:
        ordering = ['completo']
        verbose_name = 'tarea'
        verbose_name_plural = 'tareas'
    
class TareasForm(forms.ModelForm):
    user = forms.ModelChoiceField(required=False,queryset=User.objects.all(), disabled=True,label="Usuario")
    titulo = forms.CharField(required=False,disabled=True,label='Tarea')
    descripcion = forms.CharField(required=False, widget=forms.Textarea(attrs={'readonly': 'readonly'}),label="Descripcion Tarea")
    descarga = forms.URLField(required=False, disabled=False, label='Descargar archivo para firmar')
    adjunto = forms.FileField(required=False,label='Adjuntar Archivo')
    completo = forms.BooleanField(required=False,label='Tarea Realizada')
    creado = forms.DateField(required=False,disabled=True,label='Fecha de creacion')
    pv = forms.ModelChoiceField(required=False,queryset=Preventa.objects.all(), disabled=True,label="Preventa")
    
    class Meta:
        model = Tareas
        fields = '__all__'
        