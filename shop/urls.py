from django.urls import path

from . import views

urlpatterns = [
    path('', views.cart_summary, name='cart_summary'),
    path('add/<int:giftcard_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:giftcard_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('recipient/', views.gift_recipient, name='gift_recipient'),
    path('payment/', views.gift_payment, name='gift_payment'),
    path('review/', views.review_order, name='review_order'),
    path('summary/', views.order_summary, name='order_summary'),
]
