from django.contrib.auth.models import AbstractUser
from django.db import models

from giftcard_portal.utils import display
from giftcards.models import GiftCardCategory


class AddressType(models.IntegerChoices):
    RESIDENTIAL = 1, "Residential"
    COMMERCIAL = 2, "Commercial"
    MAILING = 3, "Mailing"
    SHIPPING = 4, "Shipping"


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    street_address1 = models.CharField(max_length=100)
    street_address2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)

    # Note:  Name zip_code, not zip as the latter is a built-in function
    zip_code = models.CharField(max_length=10)
    address_type = models.IntegerField(choices=AddressType, default=1)

    def __str__(self):
        return display(f"{self.street_address1}, {self.city}, {self.state} {self.zip_code}")

    def is_valid_address(self, address):
        """
        Check if address is valid

        Look at https://www.usps.com/business/web-tools-apis/

        Future...
        """
        pass

    def compare(self, other):
        if not isinstance(other, Address):
            raise TypeError("Expected Address type")

        fields = (
            "street_address1",
            "street_address2",
            "city",
            "state",
            "zip_code",
            "address_type",
        )
        return all(getattr(self, field) == getattr(other, field) for field in fields)


class UserType(models.IntegerChoices):
    ADMIN = 1, "Admin"
    CUSTOMER = 2, "Customer"
    RECIPIENT = 3, "Recipient"


class CustomUser(AbstractUser):
    """
    Contains attributes or fields:
    * id = models.AutoField(...)  # An int
    * username = models.CharField(...)
    * password = ...
    * first_name = models.CharField(...)
    * last_name = models.CharField(...)
    * email = models.EmailField(...)
    """

    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, default="", blank=True, null=True
    )
    preferred_category = models.IntegerField(choices=GiftCardCategory, blank=True, null=True)
    role = models.IntegerField(choices=UserType, default=2)
    """
    * Reference is in ShoppingCart class:
    cart = models.OneToOneField(ShoppingCart, on_delete=models.CASCADE)

    * Reference is in Payment class:
    payment_set = models.ForeignKey(Payment, on_delete=models.CASCADE)

    Contains methods:
    * set_password(password)
    * check_password(password)
    * email_user(subject, message, from_email)
    """
