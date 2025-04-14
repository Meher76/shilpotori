from django.shortcuts import render
from .models import *
#from shop.models import Product
#from .forms import ProductForm
from django.shortcuts import redirect


# Create your views here.
def home(request):
    return render(request,template_name='shop/home.html')
def products(request):
    posts = Product.objects.all()
    context = {'posts':posts}
    return render(request,template_name='shop/products.html',context=context)

def product_details(request):
    return render(request,template_name='shop/product_details.html')


