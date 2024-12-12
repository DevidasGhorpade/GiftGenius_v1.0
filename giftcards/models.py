from datetime import datetime, timedelta
from django.db import models

from giftcard_portal.utils import display


class GiftCardError(Exception):
    pass

class InactiveError(GiftCardError):
    pass

class InsufficientFundsError(GiftCardError):
    pass

class InvalidDeliveryDateError(GiftCardError):
    pass

class GiftCardCategory(models.IntegerChoices):
    BABY = 1, 'Baby'
    BIRTHDAY = 2, 'Birthday'
    BOOKS = 3, 'Books'
    CLOTHING = 4, 'Clothing'
    ELECTRONICS = 5, 'Electronics'
    ENTERTAINMENT = 6, 'Entertainment'
    FATHERSDAY = 7, 'Fathers Day'
    MOTHERSDAY = 8, 'Mothers Day'
    RETAIL = 9, 'Retail'
    TRAVEL = 10, 'Travel'
    WEDDING = 11, 'Wedding'

class CardType(models.IntegerChoices):
    DIGITAL = 1, 'Digital'
    PHYSICAL = 2, 'Physical'

class GiftCardType(models.Model):
    card_type_id = models.AutoField(primary_key=True)
    card_name = models.CharField(max_length=100)
    card_description = models.TextField()
    card_category = models.IntegerField(choices=GiftCardCategory)
    card_type = models.IntegerField(choices=CardType)
    card_quantity = models.PositiveIntegerField()
    card_image_url = models.URLField(max_length=500, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    cashback = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    vendor = models.CharField(max_length=50)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    '''
    # Reference is in BaseGiftCard class:
    basegiftcard_set = models.ForeignKey('BaseGiftCard', on_delete=models.CASCADE)
    '''

    def __str__(self):
        return display(self.card_name)

class GiftCardStatus(models.IntegerChoices):
    ACTIVE = 1, 'Active'
    INACTIVE = 2, 'Inactive'
    REDEEMED = 3, 'Redeemed'
    EXPIRED = 4, 'Expired'

class BaseGiftCard(models.Model):
    card_id = models.AutoField(primary_key=True)
    card_number = models.CharField(max_length=50, unique=True)
    cvv = models.CharField(max_length=4)
    card_holder_name = models.CharField(max_length=100)
    card_holder_address = models.OneToOneField('accounts.Address', on_delete=models.CASCADE)
    balance = models.FloatField()
    gift_message = models.TextField()
    status = models.IntegerField(choices=GiftCardStatus, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateField()
    update_date = models.DateField()

    def __str__(self):
        return f'{self.card_number} ({GiftCardStatus(self.status).label})'

    def activate(self, cardnumber: str):
        if self.gift_card_status != GiftCardStatus.EXPIRED:
            self.gift_card_status = GiftCardStatus.ACTIVE
            self.save()

    def deactivate(self):
        self.gift_card_status = GiftCardStatus.INACTIVE
        self.save()

    def redeem(self, amount: float):
        if self.gift_card_status != GiftCardStatus.ACTIVE:
            raise InactiveError('Card must be activated before use.')

        if amount > self.balance:
            raise InsufficientFundsError('Insufficient funds available on card.')

        self.gift_card_status = GiftCardStatus.REDEEMED
        self.balance -= amount

    def check_balance(self):
        if self.gift_card_status != GiftCardStatus.ACTIVE:
            raise InactiveError('Card must be activated before use.')

        return self.balance

class DigitalGiftCard(BaseGiftCard):
    # Note:  Django automatically appends _id to this field:
    card_type = models.ForeignKey(GiftCardType, on_delete=models.CASCADE)
    recipient = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE,
                                  related_name='digital_recipient')
    giver = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE,
                              related_name='digital_giver')
    delivery_date = models.DateField()

    def schedule_delivery_date(self, delivery_date):
        if delivery_date < datetime.now() or delivery_date > datetime.now() + timedelta(days=365):
            raise InvalidDeliveryDateError(
                'Delivery date cannot be in the past or more than a year in the future.'
            )
        self.delivery_date = delivery_date

    def send_gift_card(self):
        self.recipient.email_user('Your gift card!', self, self.giver.email)

class ShippingMethod(models.IntegerChoices):
    USPS = 1, 'US Postal Service'
    UPS = 2, 'UPS'
    FEDEX = 3, 'FedEx'
    DHL = 4, 'DHL'

class PhysicalGiftCard(BaseGiftCard):
    # Note:  Django automatically appends _id to this field:
    card_type = models.ForeignKey(GiftCardType, on_delete=models.CASCADE)
    recipient = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE,
                                  related_name='physical_recipient')
    giver = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE,
                              related_name='physical_giver')
    shipping_method = models.IntegerField(choices=ShippingMethod)

    def ship_gift_card(self):
        '''
        Future implementation...
        '''
        pass
