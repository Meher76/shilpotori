# myshop/urls.py
from django.urls import path
from . import views

urlpatterns = [
      
    path('', views.home, name='home'), 
   
    path('login/', views.login_view, name='login'),
    path('main/', views.main_view, name='main'), 
    path('signup/', views.signup_view, name='signup'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<str:category_name>/', views.category_filter, name='category_filter'),
    path('order/', views.order_page, name='order_page'), 
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('buyer-profile/', views.profile_view, name='BuyerProfile'),
    path('seller-profile/', views.profile_view, name='SellerProfile'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('upload/', views.upload_product, name='upload_product'),
    path('update/<int:id>/', views.update_product, name='update_product'),
    path('delete/<int:id>', views.delete_Product, name='delete_product'),
    path('add-product/', views.add_product, name='add_product'),
    path('help/', views.help_view, name='help'),
    path('track-order/', views.track_order, name='track_order'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order-history/', views.order_history, name='order_history'),
    path('order/confirmation/', views.order_confirmation, name='order_confirmation'),
    path('place-order/', views.place_order, name='place_order'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('product-list/', views.product_list, name='product_list'),

    
    
]
