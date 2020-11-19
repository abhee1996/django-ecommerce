from django.contrib import admin
from django.urls import path
from .views import *




urlpatterns = [
    path('', home , name="index"),
    path('about/', about, name="about"),
    path('cart/', cart_detail, name="cart_detail"),
    # path('cart/', cart, name="cart"),
    path('cart/add/<int:product_id>', add_cart, name="add_cart"),
    path('cart/remove/<int:product_id>', cart_remove, name="cart_remove"),
    path('cart/remove_product/<int:product_id>', cart_remove_product, name="cart_remove_product"),
    path('category/<slug:category_slug>', home, name="products_by_category"),
    path('category/<slug:category_slug>/<slug:product_slug>' , productDetail ,name="product_detail"),
    path('thank', thank_page, name="thank_you"),
    path('search/', search, name="search"),
    path('account/create/', signUpView, name="signup"),
    path('account/signin/', signInView, name="signin"),
    path('account/signout/', signoutView, name="signout"),

]
