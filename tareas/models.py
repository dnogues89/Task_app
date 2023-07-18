from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.


class Preventa(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True)
    preventa = models.CharField(max_length=8, help_text="Ejemplo 12345/1",unique=True)
    choises = [('C','Contado'),('F','Financiado')]
    tipo_venta = models.CharField(max_length= 15, choices=choises)
    choises = [('PF','Persona Fisica'),('PJ','Persona Juridica')]
    tipo_cliente = models.CharField(max_length=30,choices=choises)
    
    def __str__(self) -> str:
        return self.preventa
    
    
class Tareas(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True,verbose_name="Usuario")
    titulo = models.CharField(max_length=200,verbose_name="Tarea")
    descripcion = models.TextField(null=True,blank=True,verbose_name="Descripcion de la tarea")
    descarga = models.URLField(null=True,blank=True)
    adjunto = models.FileField(blank=True,null=True,verbose_name="Adjuntar archivo")
    completo = models.BooleanField(default=False,verbose_name="Tarea Realizada")
    creado = models.DateField(auto_now_add=True,verbose_name="Fecha de creacion")
    pv = models.ForeignKey(Preventa, on_delete=models.SET_NULL, null=True,blank=True,verbose_name="Preventa")
    
    def __str__(self) -> str:
        return self.titulo
    
    class Meta:
        ordering = ['completo']
    
class TareasForm(forms.ModelForm):
    user = forms.ModelChoiceField(required=False,queryset=User.objects.all(), disabled=True,label="Usuario")
    titulo = forms.CharField(required=False,disabled=True,label='Tarea')
    descripcion = forms.CharField(required=False, widget=forms.Textarea(attrs={'readonly': 'readonly'}),label="Descripcion Tarea")
    descarga = forms.URLField(required=False, disabled=True, label='Descargar archivo para firmar')
    adjunto = forms.FileField(required=False,label='Adjuntar Archivo')
    completo = forms.BooleanField(required=False,label='Tarea Realizada')
    #creado = forms.DateField(required=False,disabled=True,label='Fecha de creacion')
    pv = forms.ModelChoiceField(required=False,queryset=Preventa.objects.all(), disabled=True,label="Preventa")
    
    class Meta:
        model = Tareas
        fields = ['user','pv','titulo','descripcion','adjunto','completo','descarga']

    