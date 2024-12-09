from django.urls import path
from . import views

urlpatterns = [
    path('', views.giftcard_list, name='giftcard_list'),
    path('giftcard_detail/<int:card_type_id>/', views.giftcard_detail, name='giftcard_detail'),
]
