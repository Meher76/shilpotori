from django.db import models
from django.conf import settings  # Import settings to reference the custom user model
from django.apps import apps  # To use get_model instead of direct imports
from django_resized import ResizedImageField
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(blank=True, null=True)
    material = models.TextField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = ResizedImageField(
        size=[800, 800],
        quality=75,
        upload_to='products/',
        force_format='JPEG',
        blank=True,
        null=True
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Seller(models.Model):  # Class names should be Capitalized by convention
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    posted_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Order(models.Model):
    # Using apps.get_model to avoid circular imports
    product = models.ForeignKey('myshop.Product', on_delete=models.CASCADE)  # Use the app label 'myshop' to reference Product
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Add these fields
    
    first_name = models.CharField(max_length=100, null=True, blank=True, default="")
    last_name = models.CharField(max_length=100, null=True, blank=True, default="")
    phone = models.CharField(max_length=20, null=True, blank=True, default="")
    location = models.CharField(max_length=255, null=True, blank=True, default="")

    # Reference the user model dynamically
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} for {self.product.name}"










