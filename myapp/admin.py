# Open your local project ──> myapp/admin.py

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from unfold.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm
from .models import Product, Photo, PaymentTransaction, Note, SensorReading, StockMarketReading

# 🚀 FORCE-UNREGISTER BUILT-IN USER CONFIGURATIONS
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

# 🚀 RE-REGISTER SYSTEM USER USING EXPLICIT ENFOLD PASSTHROUGHS
@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm # Handles password token rendering
    
    # Mirror the default core layouts cleanly inside Unfold's Tailwind templates
    fieldsets = BaseUserAdmin.fieldsets
    add_fieldsets = BaseUserAdmin.add_fieldsets


# 🚀 REGISTER YOUR COMMERCIAL APPLIANCE LAYOUTS BEAUTIFULLY
@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['title', 'price', 'item_location', 'weight', 'is_featured', 'created_at']
    list_filter = ['item_location', 'condition', 'is_featured']
    search_fields = ['title', 'description']

@admin.register(Photo)
class PhotoAdmin(ModelAdmin):
    list_display = ['product', 'created_at']

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(ModelAdmin):
    list_display = ['tx_ref', 'product', 'amount', 'status', 'created_at']
    list_filter = ['status']

# Simple default views for secondary tracking components
admin.site.register(Note)
admin.site.register(SensorReading)
admin.site.register(StockMarketReading)
