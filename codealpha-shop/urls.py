from django.urls import path
from . import views

urlpatterns = [

    # HOME
    path("", views.home, name="home"),

    # CATEGORIES
    path("collections/", views.category_list, name="category_list"),
    path("collections/<slug:slug>/", views.category_detail, name="category_detail"),

    # PRODUCT
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),

    # AUTH
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # CART
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:product_id>/", views.cart_remove, name="cart_remove"),

    # CHECKOUT
    path("checkout/", views.checkout, name="checkout"),
]





