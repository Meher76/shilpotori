from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class Category(models.Model):  # Fixed spelling & capitalization
    name = models.CharField(max_length=100)

    def __str__(self):
      return self.name


class Product(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(default="No content available")
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    status_choices = (
        ('draft','draft'),
        ('post','post'),
    )

    status = models.CharField(max_length=50, choices=status_choices, default='default')

    def __str__(self):
      return self.title
