from django.db import models

from accounts.models import CustomUser
from giftcards.models import GiftCardType, GiftCardStatus
from giftcard_portal.utils import display

class ShoppingCart(models.Model):
    cart_id = models.AutoField(primary_key=True)

    # Note:  Django automatically appends _id to this field:
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    order_total = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.user}({self.cart_id})'

    def add_item(self, giftcard, quantity):
        if quantity > giftcard.card_quantity:
            raise ValueError(f"Only {giftcard.card_quantity} units of {giftcard.card_name} are available.")

        if existing_item := self.cart_items.filter(card_type=giftcard).first():
            existing_item.quantity += quantity
            existing_item.save()
        else:
            ShoppingCartItem.objects.create(cart=self, card_type=giftcard, quantity=quantity)

        self.update_order_total()

    def remove_item(self, giftcard):
        self.cart_items.filter(card_type=giftcard).delete()
        self.update_order_total()

    def update_order_total(self):
        self.order_total = sum(
            item.quantity * item.card_type.amount for item in self.cart_items.all()
        )
        self.save()

    def validate_cart(self):
        for item in self.cart_items.all():
            if item.quantity > item.card_type.card_quantity:
                raise ValueError(f"Insufficient stock for {item.card_type.card_name}")

    def clear_cart(self):
        self.cart_items.all().delete()
        self.update_order_total()

    def get_items(self):
        return self.cart_items.all()


class ShoppingCartItem(models.Model):
    item_id = models.AutoField(primary_key=True)

    # Note:  Django automatically appends _id to this field:
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='cart_items')

    # Note:  Django automatically appends _id to this field:
    card_type = models.ForeignKey(GiftCardType, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{display(self.card_type.card_name)} x {self.quantity}'

    def total_cost(self):
        return self.quantity * self.card_type.amount


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
    card_holder_name = models.CharField(max_length=100)

    # Note:  Django automatically appends _id to this field:
    card_holder_address = models.OneToOneField('accounts.Address', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return display(self.name)

    def validate_payment_method(self):
        pass


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    payment_method = models.OneToOneField(PaymentMethod, on_delete=models.SET_NULL, null=True)

    # Note:  Django automatically appends _id to this field:
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    '''
    # Reference is in Order class:
    order_id = models.OneToOneField(Order, on_delete=models.CASCADE)
    '''
    amount = models.FloatField()
    status = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return (
            f'{self.user.username}({self.payment_id}):  {self.amount:,.2f} on '
            f'{self.payment_method.name}'
        )

    def process_payment(self):
        if self.payment_method and self.amount > 0:
            self.status = "Completed"
            self.save()
            return True

        return False


class OrderStatus(models.IntegerChoices):
    PENDING = 1, 'Pending'
    PROCESSING = 2, 'Processing'
    SHIPPED = 3, 'Shipped'
    COMPLETED = 4, 'Completed'
    CANCELLED = 5, 'Cancelled'


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)

    # Note:  Django automatically appends _id to this field:
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    '''
    # Reference is in OrderItem class:
    item_id = models.ForeignKey(OrderItem, on_delete=CASCADE)
    '''
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.IntegerField(choices=OrderStatus, default=1)
    order_total = models.FloatField(default=0.0)

    # Note:  Django automatically appends _id to this field:
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    # Note:  Django automatically appends _id to this field:
    recipient = models.OneToOneField(
        'accounts.CustomUser', on_delete=models.CASCADE, related_name='recipient'
    )

    def __str__(self):
        return (
            f'{self.user.username}({self.order_id}):  {self.order_total:,.2f} '
            f'for {self.recipient.username}'
        )

    def update_order_total(self):
        self.order_total = sum(
           item.quantity * item.card_id.amount for item in self.orderitem_set.all()
        )
        self.save()


class OrderItem(models.Model):
    item_id = models.AutoField(primary_key=True)

    # Note:  Django automatically appends _id to this field:
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # Note:  Django automatically appends _id to this field:
    card = models.ForeignKey('giftcards.BaseGiftCard', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.card.card_number} ({GiftCardStatus(self.card_id.status).label})'
