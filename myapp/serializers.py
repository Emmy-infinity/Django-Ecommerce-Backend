from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note, SensorReading, StockMarketReading, Photo


class PhotoSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['id', 'image']

    def get_image(self, obj):
        if obj.image:
            url = obj.image.url
            # Force the URL to start explicitly with https://
            if url.startswith('//'):
                return f"https:{url}"
            return url
        return None


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "author"]
        extra_kwargs = {"author": {"read_only": True}}


class SensorReadingSerializer(serializers.ModelSerializer):
    x = serializers.DateTimeField(source='timestamp', format='%Y-%m-%d %H:%M:%S')
    y = serializers.FloatField(source='value')

    class Meta:
        model = SensorReading
        fields = ['x', 'y']
