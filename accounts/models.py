from django.contrib.auth.models import AbstractUser
from django.db import models

from giftcard_portal.utils import display


class AddressType(models.IntegerChoices):
    RESIDENTIAL = 1
    COMMERCIAL = 2
    MAILING = 3
    SHIPPING = 4


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.OneToOneField(
        'CustomUser', on_delete=models.CASCADE, default='', blank=True, null=True
    )
    streetaddress1 = models.CharField(max_length=100)
    streetaddress2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=10)
    addresstype = models.IntegerField(choices=AddressType, default=1)

    def __str__(self):
        return display(self.streetaddress1)

    def isValidAddress(self, address):
        '''
        Check if address is valid

        Look at https://www.usps.com/business/web-tools-apis/
        '''
        pass


class UserType(models.IntegerChoices):
    ADMIN = 1
    CUSTOMER = 2
    RECIPIENT = 3


class CustomUser(AbstractUser):
    '''
    Contains attributes or fields:
    * id = models.AutoField(...)  # An int
    * username = models.CharField(...)
    * password = ...
    * first_name = models.CharField(...)
    * last_name = models.CharField(...)
    * email = models.EmailField(...)
    '''

    '''
    # Don't want here - instead put in Address:
    address = models.OneToOneField(
        Address, on_delete=models.CASCADE, default='', blank=True
    )
    '''

    role = models.IntegerField(choices=UserType, default=2)
    shippingaddress = models.OneToOneField(
        Address,
        on_delete=models.CASCADE,
        related_name='shippingaddress',
        default='',
        blank=True,
        null=True
    )

    '''
    # Reference is in ShoppingCart class:
    cartid = models.OneToOneField(ShoppingCart, on_delete=models.CASCADE)

    # Reference is in Payment class:
    paymentid = models.ForeignKey(Payment, on_delete=models.CASCADE)
    '''

    '''
    Contains methods:
    * set_password(password)
    * check_password(password)
    * email_user(subject, message, from_email)
    '''
