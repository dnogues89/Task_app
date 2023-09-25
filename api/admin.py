from django.contrib import admin
from .models import CRMUpdates

# Register your models here.
class CRMUpdatesAdmin(admin.ModelAdmin):
    list_display = ('tipo','date',)

admin.site.register(CRMUpdates,CRMUpdatesAdmin)