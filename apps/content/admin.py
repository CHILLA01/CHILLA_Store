from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Model, SellerProfile, BuyerProfile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'icon_preview']
    readonly_fields = ['icon_preview']

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="50" style="border-radius: 5px;" />', obj.icon.url)
        return "No Image"

@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'category', 'image_preview']
    list_filter = ['category']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="50" style="border-radius: 5px;" />', obj.image.url)
        return "No Image"

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar_preview']
    readonly_fields = ['avatar_preview']

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="40" style="border-radius: 20px;" />', obj.avatar.url)
        return "No Image"

@admin.register(BuyerProfile)
class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar_preview']
    readonly_fields = ['avatar_preview']


    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="40" style="border-radius: 20px;" />', obj.avatar.url)
        return "No Image"