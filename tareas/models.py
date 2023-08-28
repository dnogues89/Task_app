from typing import Any, Dict, Iterable, Optional, Tuple
import os
from django.db import models
from django import forms
from django.contrib.auth.models import User

def check_preventa_completa(instance):
    if Tareas.objects.filter(pv=instance.pv, completo=False).count()==0:
        preventa = Preventa.objects.get(preventa=instance.pv)
        if preventa.retira_unidad != "" and preventa.socios != None and preventa.cedulas_azules != None:
            print(preventa.socios)
            preventa.completo = True
            preventa.save()
        
    

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
    tipo_venta = models.CharField(max_length= 15, choices=choises) # agregar tareas a ==l tipo de venta, no lo hace CARVAJAL desde la API!
    choises = [('Persona Fisica','Persona Fisica'),('Persona Juridica','Persona Juridica')] 
    tipo_cliente = models.CharField(max_length=30,choices=choises, blank=True, null=True)
    choises = [('Soltero/a','Soltero/a'),('Casado/a','Casado/a')] 
    estado_civil = models.CharField(max_length=30,choices=choises,blank=True, null=True) #Agregar tareas al estado civil
    choises = [('No','No'),('Si','Si')]
    co_titular = models.CharField(max_length=2, choices=choises, blank=True,null=True)
    cedulas_azules = models.IntegerField(blank=True,null=True)
    socios = models.IntegerField(blank=True,null=True)
    choises = [('Transportista','Transportista'),('Individuo','Individuo'),('Titular','Titular')]
    retira_unidad = models.CharField(max_length= 15, choices=choises, blank=True,null=True)
    contado = models.BooleanField(null=True)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, null=True,blank=True)
    completo=models.BooleanField(default=False)
    fecha_inicio = models.DateTimeField(auto_now=True,verbose_name='Fecha de creacion')
    
    def __str__(self) -> str:
        return self.preventa

class PreventaForm(forms.ModelForm):
    user = forms.ModelChoiceField(required=False,queryset=User.objects.all(), disabled=True,label="Usuario")
    preventa = forms.CharField(required=False,disabled=True,label='Numero de Preventa')
    choises = [('Persona Fisica','Persona Fisica'),('Persona Juridica','Persona Juridica')]
    tipo_cliente = forms.ChoiceField(choices= choises, required=False, disabled=False, label='Tipo de cliente final')
    choises = [('Soltero/a','Soltero/a'),('Casado/a','Casado/a')] 
    estado_civil = forms.ChoiceField(choices= choises, required=False, disabled=False, label='Estado Civil TITULAR')
    choises = [('No','No'),('Si','Si')]
    co_titular = forms.ChoiceField(choices= choises, required=False, disabled=False, label='Co-Titular')
    cedulas_azules = forms.IntegerField(required=False, label='Cantidad cedulas azules. En numero')
    socios = forms.IntegerField(required=False,label='Si es SS o SH indicar cantidad de socios involucrados')
    choises = [('',''),('Transportista','Transportista'),('Individuo','Individuo'),('Titular','Titular')]
    retira_unidad = forms.ChoiceField(choices= choises, required=False, disabled=False, label='Quien retira la unidad?')
    # vendedor = forms.ModelChoiceField(required=False,queryset=Vendedor.objects.all(), disabled=True)
    completo = forms.BooleanField(required=False, label='Operacion terminada.')
 
    
    class Meta:
        model = Preventa
        fields = '__all__'
    
    
    
class Tareas(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(null=True,blank=True)
    descarga = models.CharField(max_length=30,null=True,blank=True)
    adjunto = models.FileField(blank=True,null=True,upload_to=save_path)
    completo = models.BooleanField(default=False)
    actualizado = models.DateField(auto_now=True) # fecha de actualizacion para 
    creado = models.DateField(auto_now_add=True)
    pv = models.ForeignKey(Preventa, on_delete=models.CASCADE, null=True,blank=True)
    
    def __str__(self) -> str:
        return self.titulo
    
    def save(self, *args, **kwargs):
        try:
            # Verificar si se está modificando una instancia existente.
            if self.pk is not None:
                
                
                # Obtener el objeto existente de la base de datos.
                old_obj = Tareas.objects.get(pk=self.pk)
                # Verificar si el archivo adjunto ha sido modificado.
                if old_obj.adjunto != self.adjunto:
                    # Eliminar el archivo adjunto anterior si ha sido modificado.
                    old_obj.adjunto.delete(save=False)
                    _,ext = os.path.splitext(os.path.basename(self.adjunto.name))
                    self.adjunto.name = f'{self.titulo}{ext}'
                    self.completo = True
        except:
            pass    
        # Guardar la instancia del modelo con el nuevo archivo adjunto.
        super().save(*args, **kwargs)
        if self.pk is not None:
            tarea = Tareas.objects.get(pk=self.pk)
            check_preventa_completa(tarea)


    
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
    descarga = forms.CharField(required=False, disabled=False, label='Descargar archivo para firmar')
    adjunto = forms.FileField(required=False,label='Adjuntar Archivo')
    completo = forms.BooleanField(required=False,label='Tarea Realizada')
    pv = forms.ModelChoiceField(required=False,queryset=Preventa.objects.all(), disabled=True,label="Preventa")
    
    class Meta:
        model = Tareas
        fields = "__all__"
        
class TipoTarea(models.Model):
    tipo = models.CharField(max_length=200)

class AsignacionTareas(models.Model):
    tipo = models.ForeignKey(TipoTarea, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=250)
    descipcion = models.TextField()
    