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



