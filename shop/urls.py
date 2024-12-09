from django.urls import path
from . import views
from .views import ShopPageView

urlpatterns = [
    path('', views.cart_summary, name='shop'),
    path('shop/', views.cart_summary, name='cart_summary'),
    path('shop/add/<int:giftcard_id>/', views.add_to_cart, name='add_to_cart'),
    path('shop/remove/<int:giftcard_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout')
]