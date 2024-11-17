from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    '''
    Contains:
    * username = models.CharField(...)
    * password = ...
    * first_name = models.CharField(...)
    * last_name = models.CharField(...)
    * email = models.EmailField(...)
    * is_active = models.BooleanField(...)
    * is_staff = models.BooleanField(...)
    * is_superuser = models.BooleanField(...)
    * date_joined = models.DateTimeField(...)
    * last_login = models.DateTimeField(...)

    To add:
    * address = Address (user class)
    * shippingaddress = Address (user class)
    * role = UserType (enum)
    '''
    class UserType(models.IntegerChoices):
        ADMIN = 1
        CUSTOMER = 2
        RECIPIENT = 3

    usertype = models.IntegerField(choices=UserType, default=2)
