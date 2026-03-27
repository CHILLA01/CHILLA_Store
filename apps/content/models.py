import uuid
import os
from django.db import models
from django.contrib.auth.models import User


def category_icon_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('category_icons/', filename)

def model_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('model_images/', filename)

def profile_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('avatars/', filename)


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    icon = models.ImageField(upload_to=category_icon_path, null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Model(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='models')
    image = models.ImageField(upload_to=model_image_path, null=True, blank=True)

    class Meta:
        ordering = ['name', 'price']

    def __str__(self):
        return self.name


class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to=profile_avatar_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Seller: {self.user.username}"


class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_profile')
    address = models.TextField(blank=True)
    avatar = models.ImageField(upload_to=profile_avatar_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Buyer: {self.user.username}"