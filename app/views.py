from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def home(request, c_slug=None):
    products = None
    if c_slug != None:
        c_page = get_object_or_404(Category, slug=c_slug)
        products = Products.objects.filter(category=c_page, available=True)

    else:
        products = Products.objects.all().filter(available=True)

    category = Category.objects.all()
    paginator = Paginator(products, 12)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        product = paginator.page(page)
    except(EmptyPage, InvalidPage):
        product = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'products': product, 'category': category, })


def product_details(request, c_slug, p_slug):
    category = Category.objects.all()
    try:
        product = Products.objects.get(category__slug=c_slug, slug=p_slug)

    except Exception as e:
        raise e
    return render(request, 'product.html', {'product': product, 'category': category})


def search(request):
    category = Category.objects.all()
    products = None
    query = None
    if 'search' in request.GET:
        query = request.GET.get('search')
        products = Products.objects.all().filter(Q(name__contains=query) | Q(description__contains=query))
    return render(request, 'search.html', {'query': query, 'products': products, 'category': category})


# def ct_id(request):
#     ct_id = request.session.session_key
#     if not ct_id:
#         request.session.create()
#         ct_id = request.session.session_key
#     return ct_id
def ct_id(request):
    # Check if the session key is already available
    if 'ct_id' not in request.session:
        # If not, create a new session key
        request.session['ct_id'] = request.session.session_key or 'default_cart_id'
    return request.session['ct_id']


@login_required
def cart(request, total=0, count=0, ct_items=None):
    category = Category.objects.all()
    try:
        ct = CartList.objects.get(cart_id=ct_id(request))
        ct_items = Item.objects.filter(cart=ct,user=request.user, active=True)
        # ct_items = Item.objects.filter(active=True)  will not work properly
        for i in ct_items:
            total += i.product.price * i.quantity
            count += i.quantity
    except ObjectDoesNotExist:
        pass
    return render(request, 'cart.html', {'cart_items': ct_items, 'total': total, 'count': count, 'category': category})


def add_cart(request, product_id):
    product = Products.objects.get(id=product_id)
    try:
        ct = CartList.objects.get(cart_id=ct_id(request))
    except CartList.DoesNotExist:
        ct = CartList.objects.create(cart_id=ct_id(request))
        ct.save()

    try:
        c_items = Item.objects.get(product=product, cart=ct,user=request.user)
        if c_items.quantity < c_items.product.stock:
            c_items.quantity += 1

        c_items.save()

    except Item.DoesNotExist:
        c_items = Item.objects.create(product=product, quantity=1, cart=ct,user=request.user)
        c_items.save()

    return redirect("cart")


def min_cart(request, product_id):
    ct = CartList.objects.get(cart_id=ct_id(request))
    product = get_object_or_404(Products, id=product_id)
    ct_items = Item.objects.get(product=product, cart=ct,user=request.user)

    if ct_items.quantity > 1:
        ct_items.quantity -= 1
        ct_items.save()
    else:
        ct_items.delete()

    return redirect('cart')


def cart_delete(request, product_id):
    ct = CartList.objects.get(cart_id=ct_id(request))
    product = get_object_or_404(Products, id=product_id)
    ct_items = Item.objects.get(product=product, cart_id=ct,user=request.user)
    ct_items.delete()
    return redirect('cart')


from django.contrib.auth import authenticate, login as auth_login


def log_in(request):
    category = Category.objects.all()

    if request.method == 'POST':
        # Handle form submission
        username = request.POST.get('Username')
        password = request.POST.get('password')

        # Debugging: Print out username and password
        print("Username:", username)
        print("Password:", password)

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print('User authenticated. Redirecting to home.')
            return redirect('home')
        else:
            # Authentication failed, handle invalid credentials error
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html', {"category": category})


def register(request):
    category = Category.objects.all()
    if request.method == 'POST':
        # Handle form submission
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('Username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Check if passwords match
        if password1 != password2:
            # Handle password mismatch error
            # You can render the registration page with an error message
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html', {'category': category})

        try:
            # Create a new user
            user = User.objects.create_user(username=username, email=email, password=password1, first_name=firstname,
                                            last_name=lastname)
        except IntegrityError:
            # If username is not unique, inform the user
            messages.error(request, 'Username already exists. Please choose a different username.')
            return render(request, 'register.html', {'category': category})

        # Authenticate the user
        user = authenticate(username=username, password=password1)

        # Check if user authentication was successful
        if user is not None:
            login(request, user)
            print('User authenticated. Redirecting to home.')
            return redirect('home')
        else:
            # Authentication failed, handle error
            messages.error(request, 'Failed to authenticate user after registration')
            return render(request, 'register.html', {'category': category})

    # If the request method is GET, render the registration page template
    return render(request, 'register.html', {'category': category})


def log_out(request):
    logout(request)
    return redirect('home')