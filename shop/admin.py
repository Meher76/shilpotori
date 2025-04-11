from django.contrib import admin
#from unicodedata import category

from .models import *
# Register your models here.
admin.site.register([Product,Category])