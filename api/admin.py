from django.contrib import admin

# Register your models here.
from .models import Device, Deployment, Alert

admin.site.register(Device)
admin.site.register(Deployment)
admin.site.register(Alert)
