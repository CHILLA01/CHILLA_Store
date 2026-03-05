from django.contrib import admin
from .models import Category, Model


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'category']
    list_filter = ['category']
    search_fields = ['name', 'description']
