from django.contrib import admin
from .models import CRMUpdates, UploadErrors

# Register your models here.
class CRMUpdatesAdmin(admin.ModelAdmin):
    list_display = ('tipo','date',)

class UploadLogsAdmin(admin.ModelAdmin):
    list_display = ('tipo','preventa','date',)
    

admin.site.register(CRMUpdates,CRMUpdatesAdmin)
admin.site.register(UploadErrors,UploadLogsAdmin)