from django import forms
from .models import UserProfile, Product
from django.forms import ModelForm
from users.models import CustomUser

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'phone', 'address', 'profile_picture']


       
class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'user_type', 'password']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'quantity', 'material', 'price', 'category', 'image']           


   