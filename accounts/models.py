from django.contrib.auth.models import AbstractUser
from django.db import models


class Address(models.Model):
    # id = models.AutoField(primary_key=True)
    userid = models.OneToOneField(
        'CustomUser', on_delete=models.CASCADE, default='', blank=True, primary_key=True
    )
    streetaddress1 = models.CharField(max_length=100)
    streetaddress2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=10)

    class AddressType(models.IntegerChoices):
        RESIDENTIAL = 1
        COMMERCIAL = 2
        MAILING = 3
        SHIPPING = 4

    addresstype = models.IntegerField(choices=AddressType, default=1)

    def __str__(self):
        return (
            self.streetaddress1[:30]
            if len(self.streetaddress1) <= 30
            else f'{self.streetaddress1[:27]}...'
        )


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
    '''

    '''
    address = models.OneToOneField(
        Address, on_delete=models.CASCADE, default='', blank=True
    )
    '''

    class UserType(models.IntegerChoices):
        ADMIN = 1
        CUSTOMER = 2
        RECIPIENT = 3

    role = models.IntegerField(choices=UserType, default=2)
    shippingaddress = models.OneToOneField(
        Address,
        on_delete=models.CASCADE,
        related_name='shippingaddress',
        default='',
        blank=True,
        null=True
    )
