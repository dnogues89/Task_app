from django.contrib import admin
from .models import Tareas, Preventa, TareasPreventa


# Register your models here.
admin.site.register(Tareas)
admin.site.register(Preventa)
admin.site.register(TareasPreventa)