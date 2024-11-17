from django.urls import path

from .views import ShopPageView

urlpatterns = [
    path('', ShopPageView.as_view(), name='shop')
]
