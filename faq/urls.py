from django.urls import path

from . import views

urlpatterns = [path("", views.display_faq, name="display_faq")]
