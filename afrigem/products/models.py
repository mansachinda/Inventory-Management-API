from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='product_images', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)


    def __str__(self):
        return self.name