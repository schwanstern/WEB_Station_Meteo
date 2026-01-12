from django.contrib import admin
from .models import AlertSettings, SensorFallback

admin.site.register(AlertSettings)
admin.site.register(SensorFallback)
