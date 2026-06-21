from django.db import models
from django.contrib.auth.models import User


# models.py
from django.db import models
from cloudinary.models import CloudinaryField

class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = CloudinaryField('image') # Handles Cloudinary upload directly



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
    timestamp=models.DateTimeField(auto_created=True)
    value1=models.FloatField()
    value2=models.FloatField()
    
    
    
