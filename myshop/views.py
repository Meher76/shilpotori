from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category, UserProfile, Order
from .forms import ProfileForm, ProductForm
from django.http import JsonResponse
import json
from django.http import HttpResponseForbidden





def home(request):
    return render(request, 'home.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')  # Add this line

        User = get_user_model()
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')
        user = User.objects.create_user(username=username, email=email, password=password, user_type=user_type)  # Pass user_type here
        login(request, user)
        return redirect('main')
    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def main_view(request):
    return render(request, 'main.html')

def category_list(request):
    products = Product.objects.all()
    return render(request, 'categories.html', {'products': products, 'filter': 'All Products'})

def category_filter(request, category_name):
    category = Category.objects.filter(name__iexact=category_name).first()
    products = Product.objects.filter(category=category) if category else []
    return render(request, 'categories.html', {'products': products, 'filter': category_name})





def order_confirmation(request, order_id):
    # Fetch the order using the order_id
    order = get_object_or_404(Order, id=order_id)

    # Pass the order object to the template
    return render(request, 'order_confirmation.html', {'order': order})





def confirm_order(request):
    if request.method == 'POST':
        product = Product.objects.get(id=request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity'))
        total_price = float(request.POST.get('total_price'))

        Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_price=total_price,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            phone=request.POST.get('phone'),
            location=request.POST.get('location')
        )

        return redirect('main')


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-ordered_at')
    return render(request, 'order_history.html', {'orders': orders})





@login_required
def place_order(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity"))
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone = request.POST.get("phone")
        location = request.POST.get("location")
        unit_price = float(request.POST.get("unit_price"))
        total_price = float(request.POST.get("total_price"))
        
        # Get the product
        product = Product.objects.get(id=product_id)

        # Create a new order
        order = Order.objects.create(
            product=product,
            quantity=quantity,
            total_price=total_price,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            location=location,
            user=request.user  # Automatically link the order to the logged-in user
        )

        # Redirect to the order confirmation page (you can define the URL pattern for order confirmation)
        return redirect('order_confirmation', order_id=order.id)

    # If it's not a POST request, render the order page
    return render(request, 'order_page.html')





@login_required
def profile_view(request):
    user = request.user
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None

    if request.method == "POST":
        full_name = request.POST.get('full_name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        bio = request.POST.get('bio')
        address = request.POST.get('address')
        # Handle profile picture upload
        profile_picture = request.FILES.get('profile_picture')

        # Update user fields
        user.email = email
        if full_name:
            name_parts = full_name.split(' ')
            user.first_name = name_parts[0]
            if len(name_parts) > 1:
                user.last_name = ' '.join(name_parts[1:])
        if password:
            user.set_password(password)
        user.save()

        # Update or create profile fields
        if profile:
            profile.phone = phone
            profile.bio = bio
            profile.address = address
            if profile_picture:
                profile.profile_picture = profile_picture
            profile.save()
        else:
            profile = UserProfile.objects.create(
                user=user,
                phone=phone,
                bio=bio,
                address=address,
                profile_picture=profile_picture
            )

        messages.success(request, "Profile updated successfully!")
        return redirect('main')

    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'BuyerProfile.html', context)



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
            'image': product.image.url
        }

    request.session['cart'] = cart
    return redirect('view_cart')


def view_cart(request):
    cart = request.session.get('cart', {})
    products = []

    for product_id, item in cart.items():
        total_price = item['price'] * item['quantity']
        products.append({
            'id': product_id,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'image': item['image'],
            'total_price': total_price
        })

    return render(request, 'cart.html', {'products': products})


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart

    return redirect('view_cart')


def order_page(request):
    if request.method == 'POST':
        # handle form submission, forward to confirmation page
        context = {
            'product': Product.objects.get(id=request.POST.get('product_id')),
            'quantity': request.POST.get('quantity'),
            'total_price': request.POST.get('total_price'),
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'phone': request.POST.get('phone'),
            'location': request.POST.get('location'),
        }
        return render(request, 'order_confirmation.html', context)
    else:
        product_id = request.GET.get('product_id')
        quantity = int(request.GET.get('quantity', 1))
        unit_price = float(request.GET.get('unit_price', 0))
        product = Product.objects.get(id=product_id)
        total = quantity * unit_price

        return render(request, 'order_page.html', {
            'product': product,
            'quantity': quantity,
            'total': total,
        })





def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Redirect to order page with the necessary details
    if 'buy_now' in request.GET:  # Check if "Buy Now" was clicked
        quantity = 1  # You can get this from the form if needed
        return redirect('order_page', product_id=product.id, quantity=quantity, unit_price=product.price)
    
    return render(request, 'product_detail.html', {'product': product})



def upload_product(request):
    form =  ProductForm()
    if request.method == 'POST':
        form =  ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    context = {'form': form}
    return render(request, template_name='product_form.html', context=context)







@login_required
def update_product(request, id):
    
    product = get_object_or_404(Product, pk=id)

   
    if product.user != request.user:
        return redirect('main')  

    # If the form is submitted
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()  # Save the updated product
            return redirect('category_list') 

    else:
       
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product
    }
    return render(request, 'product_form.html', context)



@login_required
def delete_Product(request, id):  # <- Make sure 'id' is included here
    product = get_object_or_404(Product, id=id)

    if product.user != request.user:
        return redirect('main')

    if request.method == 'POST':
        product.delete()
        return redirect('category_list')  

    return render(request, 'delete_product.html', {'product': product})

def help_view(request):
    return render(request, 'help.html')




@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            
            product = form.save(commit=False)
            product.user = request.user 
            product.save()  
            return redirect('category_list') 
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})




def track_order(request):
    tracking_info = None
    error = None
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        # Replace this with your actual order lookup logic
        # Example: order = Order.objects.filter(id=order_id).first()
        if order_id == "12345":
            tracking_info = {
                "status": "Shipped",
                "eta": "2024-06-10"
            }
        else:
            error = "Order not found. Please check your Order ID."
    return render(request, "track_order.html", {
        "tracking_info": tracking_info,
        "error": error
    })
def buyer_profile_view(request):
    # Your logic here
    return render(request, 'BuyerProfile.html')

def seller_profile_view(request):
    # Your logic here
    return render(request, 'SellerProfile.html')



@login_required
def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password and new_password == confirm_password:
            user = request.user
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password updated successfully. Please log in again.')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match or are empty.')

    return render(request, 'reset_password.html') 







