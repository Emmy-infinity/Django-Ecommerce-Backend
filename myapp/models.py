from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return self.title

class Product(models.Model):
    name=models.CharField(max_length=200)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    description=models.TextField()
class ProductImage(models.Model):
    product=models.ForeignKey(Product,related_name='images',on_delete=models.CASCADE)
    image=models.ImageField(upload_to='products')
    order=models.IntegerField(default=0)
class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/' )
    title = models.CharField(max_length=100, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description=models.CharField(max_length=500,blank=True)
    
    
    class Meta:
        pass

    def __str__(self):
        return self.title or str(self.image)



class SensorReading(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()

    def __str__(self):
        return f"{self.timestamp}: {self.value}"

class StockMarketReading(models.Model):
    timestamp=models.DateTimeField(auto_created=True)
    value1=models.FloatField()
    value2=models.FloatField()
    
    
    