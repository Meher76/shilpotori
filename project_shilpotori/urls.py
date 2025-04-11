
from django.contrib import admin
from django.urls import path
from shop import views as shop_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',shop_views.home,name='home'),
    path('products/',shop_views.products,name='products'),
    path('product_details/',shop_views.product_details,name='product_details'),

]
