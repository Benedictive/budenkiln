from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Kiln)
admin.site.register(TemperatureCurve)
admin.site.register(TemperaturePoint)