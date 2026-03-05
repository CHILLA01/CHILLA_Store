from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='category/', null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Model(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='models')
    image = models.ImageField(upload_to='model/', null=True, blank=True)

    class Meta:
        ordering = ['name', 'price']

    def __str__(self):
        return self.name
