from django.urls import path
from . import views

urlpatterns = [
    path('', views.giftcard_list, name='giftcard_list'),
]
