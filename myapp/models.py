from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


User = get_user_model()

class Product(models.Model):
    CONDITION_CHOICES = [
        ('NEW', 'Brand New / Sealed'),
        ('REFURB', 'Refurbished / Tested'),
        ('USED', 'Used / Working'),
        ('SCRAP', 'Scrap / For Spare Parts'),
    ]
    
    LOCATION_CHOICES = [
        ('GULU', 'Gulu City'),
        ('LIRA', 'Lira City'),
        ('KLA', 'Kampala Road / Hub'),
        ('ARUA', 'Arua City'),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    # Financials & Inventory
    price = models.DecimalField(max_digits=12, decimal_places=2) # Supports millions of UGX safely
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='USED')
    stock_count = models.PositiveIntegerField(default=1)
    
    # Logistics
    item_location = models.CharField(max_length=10, choices=LOCATION_CHOICES, default='GULU')
    seller_location_details = models.CharField(max_length=255, help_text="e.g., Near Gulu University Main Gate")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.price:,} UGX"




class Photo(models.Model):
    # Option A: Keep CloudinaryField directly
    image = CloudinaryField('image')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photos', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    # Option B (Recommended if using cloudinary_storage storage backend):
    # image = models.ImageField(upload_to='photos/')


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
