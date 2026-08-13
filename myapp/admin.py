# admin.py
from django.contrib import admin
from .models import Product, Photo

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 3 # Gives you 3 blank image slots automatically on the product edit page

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'condition', 'item_location', 'seller', 'created_at']
    list_filter = ['condition', 'item_location', 'created_at']
    search_fields = ['title', 'description']
    inlines = [PhotoInline] # Embeds the photo uploader inside the product dashboard
