from django.db import models

# Create your models here.
class CRMUpdates(models.Model):
    tipo = models.CharField(max_length=50)
    date = models.DateField()
    
    def __str__(self) -> str:
        return self.tipo