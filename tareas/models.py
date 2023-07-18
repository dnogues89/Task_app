from django.db import models
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
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(null=True,blank=True)
    adjunto = models.FileField(blank=True,null=True)
    completo = models.BooleanField(default=False)
    creado = models.DateField(auto_now_add=True)
    pv = models.ForeignKey(Preventa, on_delete=models.SET_NULL, null=True,blank=True)
    
    def __str__(self) -> str:
        return self.titulo
    
    class Meta:
        ordering = ['completo']
        

        


    
    