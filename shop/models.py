from django.db import models

from giftcards.models import GiftCardStatus
from giftcard_portal.utils import display


class ShoppingCart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(
        # Note:  on_delete=CASCADE is more like composition than aggregation:
        'accounts.CustomUser', on_delete=models.CASCADE, blank=True, null=True
    )
    '''
    # Reference is in ShoppingCartItem class:
    item_id = models.ForeignKey(ShoppingCartItem, on_delete=CASCADE)
    '''
    order_total = models.FloatField(default=0.0)

    # Session management handled by Django - don't need where requiring current
    # user (accounts.CustomUser)

    def __str__(self):
        return f'{self.user_id}({self.cart_id})'

    def add_item(self, giftcard):
        pass

    def remove_item(self, giftcard):
        pass

    def update_order_total(self):
        pass


class ShoppingCartItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    cart_id = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    card_type_id = models.ForeignKey('giftcards.GiftCardType', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{display(self.card_type_id.card_name)} x {self.quantity}'


class PaymentMethod(models.Model):
    payment_method_id = models.AutoField(primary_key=True)
    '''
    # Reference is in Payment class:
    payment_id = models.OneToOneField(Payment, on_delete=SET_NULL, null=True)
    '''
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    card_number = models.CharField(max_length=20)
    expiration_date = models.DateTimeField()
    cvv = models.CharField(max_length=4)
    name_on_card = models.CharField(max_length=100)
    status = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return display(self.name)

    def validate_payment_method(self):
        pass


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    payment_method = models.OneToOneField(PaymentMethod, on_delete=models.SET_NULL, null=True)
    user_id = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    '''
    # Reference is in Order class:
    order_id = models.OneToOneField(Order, on_delete=models.CASCADE)
    '''
    amount = models.FloatField()
    status = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'{self.user_id.username} - {self.payment_method.name} for {self.amount:,.2f}'

    def process_payment(self):
        pass


class OrderStatus(models.IntegerChoices):
    PENDING = 1, 'Pending'
    PROCESSING = 2, 'Processing'
    SHIPPED = 3, 'Shipped'
    COMPLETED = 4, 'Completed'
    CANCELLED = 5, 'Cancelled'


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    '''
    # Reference is in OrderItem class:
    item_id = models.ForeignKey(OrderItem, on_delete=CASCADE)
    '''
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.IntegerField(choices=OrderStatus, default=1)
    order_total = models.FloatField(default=0.0)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    recipient = models.OneToOneField(
        'accounts.CustomUser', on_delete=models.CASCADE, related_name='recipient'
    )

    def __str__(self):
        return f'{self.user_id.username} for {self.recipient.username} - {self.order_total:,.2f}'

    def update_order_total(self):
        pass


class OrderItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    card_id = models.ForeignKey('giftcards.BaseGiftCard', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.card_id.card_number} ({GiftCardStatus(self.card_id.status).label})'
