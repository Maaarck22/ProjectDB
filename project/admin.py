# project/admin.py

from django.contrib import admin
from .models import Products

class ProductAdmin(admin.ModelAdmin):
    list_display = ('ProductID', 'Product_name', 'Description', 'Category', 'Price', 'Availability', 'Image')
    search_fields = ('Product_name', 'Category')

admin.site.register(Products, ProductAdmin)
