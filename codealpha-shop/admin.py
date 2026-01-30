from django.contrib import admin
from .models import Category, Product, CartItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "selling_price", "qty", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(CartItem)  # Already correct
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "qty", "created_at")
    search_fields = ("user__username", "product__name")
