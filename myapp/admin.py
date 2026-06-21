from django.contrib import admin
from .models import Note,Photo,SensorReading

# Register your models here.
admin.site.register(Note)
admin.site.register(Photo)
admin.site.register(SensorReading)
