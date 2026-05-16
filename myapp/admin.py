from django.contrib import admin
from .models import Note,UploadedImage,SensorReading

# Register your models here.
admin.site.register(Note)
admin.site.register(UploadedImage)
admin.site.register(SensorReading)