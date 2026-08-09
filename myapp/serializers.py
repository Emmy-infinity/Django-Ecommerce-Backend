from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note, SensorReading, Photo  # Import Photo model here, do not define it!

class PhotoSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['id', 'image']

    def get_image(self, obj):
        if obj.image:
            url = obj.image.url
            if url.startswith('//'):
                return f"https:{url}"
            return url
        return None

# ... rest of your serializers ...

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return self.title


class SensorReading(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()

    def __str__(self):
        return f"{self.timestamp}: {self.value}"


class StockMarketReading(models.Model):
    # Fixed auto_created=True to auto_now_add=True
    timestamp = models.DateTimeField(auto_now_add=True)
    value1 = models.FloatField()
    value2 = models.FloatField()

    def __str__(self):
        return f"{self.timestamp}: {self.value1} / {self.value2}"
