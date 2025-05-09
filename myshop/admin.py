from django.contrib import admin

from.models import *

admin.site.register([Category,Product])

from django.contrib.auth.admin import UserAdmin
#from .models import CustomUser  # or your user model

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')

#admin.site.register(CustomUser, CustomUserAdmin)
