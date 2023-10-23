from django.db import models

# Create your models here.
class CRMUpdates(models.Model):
    tipo = models.CharField(max_length=50)
    date = models.DateField()
    
    def __str__(self) -> str:
        return self.tipo

class UploadErrors(models.Model):
    tipo = models.CharField(max_length=300)
    preventa = models.CharField(max_length=50)
    date = models.DateTimeField(auto_created=True)
    log = models.TextField()
    
    def __str__(self) -> str:
        return self.preventa