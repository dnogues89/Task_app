from django.db import models
from django import forms
from django.contrib.auth.models import User


# Create your models here.


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
    completo=models.BooleanField(default=False)
    
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
    completo = forms.BooleanField(required=False, label='Operacion terminada.')
    
    
    
    class Meta:
        model = Preventa
        fields = '__all__'
    
    
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
    descarga = forms.URLField(required=False, disabled=False, label='Descargar archivo para firmar')
    adjunto = forms.FileField(required=False,label='Adjuntar Archivo')
    completo = forms.BooleanField(required=False,label='Tarea Realizada')
    #creado = forms.DateField(required=False,disabled=True,label='Fecha de creacion')
    pv = forms.ModelChoiceField(required=False,queryset=Preventa.objects.all(), disabled=True,label="Preventa")
    
    class Meta:
        model = Tareas
        fields = ['user','pv','titulo','descripcion','adjunto','completo','descarga']

class TareasPreventa(models.Model):
    preventa = models.ForeignKey(Preventa, on_delete=models.SET_NULL, null=True,blank=True,verbose_name="Preventa")
    choises = [(1,'Transportista'),(2,'Individuo'),(3,'Titular')]
    retira_unidad = models.IntegerField(max_length= 15, choices=choises, blank=True,null=True)
    cedulas_azules = models.IntegerField(blank=True,null=True)
    socios = models.IntegerField(blank=True,null=True)
    
