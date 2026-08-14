# admin.py
# myapp/admin.py
from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline # 🧠 USE THESE INSTEAD
from .models import Product, Photo

class PhotoInline(TabularInline): # Elegant responsive inline inputs
    model = Photo
    extra = 3

@admin.register(Product)
class ProductAdmin(ModelAdmin): # Inherits clean Tailwind CSS styling
    list_display = ['title', 'price', 'condition', 'item_location', 'seller']
    list_filter = ['condition', 'item_location']
    search_fields = ['title', 'description']
    inlines = [PhotoInline]

# Open your local project ──> myapp/admin.py

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from unfold.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.forms import AdminPasswordChangeForm # 🌟 CRITICAL ALIGNMENT HOOK

# 1. Unregister the built-in standard User admin layout safely
admin.site.unregister(User)

# 2. Re-register the User model using Unfold's premium Tailwind layout configuration
@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Overwrites default input structures with responsive components
    form = UserChangeForm
    add_form = UserCreationForm
    
    # 🌟 THE ABSOLUTE OVERRIDE FOR THE CRYPTOGRAPHIC FIELDS (PASTE BOTH LINES)
    change_password_form = AdminPasswordChangeForm
    
    # Enforce field validation arrays to align components cleanly inside Unfold's views
    fieldsets = BaseUserAdmin.fieldsets
    add_fieldsets = BaseUserAdmin.add_fieldsets
