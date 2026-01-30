from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product, Category, CartItem
from .forms import RegisterForm


def home(request):
    products = Product.objects.filter(is_active=True)[:8]
    return render(request, "shop/home.html", {"products": products})




def category_list(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, "shop/collections.html", {"categories": categories})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = category.products.filter(is_active=True)
    return render(request, "shop/category_products.html",
                  {"category": category, "products": products})



def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "shop/product_detail.html", {"product": product})




def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("shop:home")
    else:
        form = RegisterForm()
    return render(request, "shop/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect("shop:home")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "shop/login.html")


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("shop:home")




@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.qty += 1
        item.save()
    messages.success(request, "Product added to cart.")
    return redirect("shop:cart")


@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user)
    sub_total = sum(i.sub_total() for i in items)
    return render(request, "shop/cart.html", {"items": items, "sub_total": sub_total})


@login_required
def cart_remove(request, product_id):
    item = get_object_or_404(CartItem, user=request.user, product_id=product_id)
    item.delete()
    messages.info(request, "Product removed from cart.")
    return redirect("shop:cart")


@login_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user)
    if not items:
        messages.info(request, "Your cart is empty.")
        return redirect("shop:cart")
    sub_total = sum(i.sub_total() for i in items)
    return render(request, "shop/checkout.html", {"items": items, "sub_total": sub_total})
