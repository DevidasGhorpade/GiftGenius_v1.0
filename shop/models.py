from django.db import models

from giftcard_portal.utils import display


class ShoppingCart(models.Model):
    cartid = models.AutoField(primary_key=True)
    userid = models.OneToOneField(
        # Note:  on_delete=CASCADE is more like composition than aggregation:
        'accounts.CustomUser', on_delete=models.CASCADE, blank=True, null=True
    )
    '''
    # Reference is in ShoppingCartItem class:
    itemid = models.ForeignKey(ShoppingCartItem, on_delete=CASCADE)
    '''
    orderTotal = models.FloatField(default=0.0)

    # Session management handled by Django - don't need where requiring current
    # user (accounts.CustomUser)

    def __str__(self):
        return f'{self.userid}({self.cartid})'

    def addItem(self, giftcard):
        pass

    def removeItem(self, giftcard):
        pass

    def updateOrderTotal(self):
        pass


class ShoppingCartItem(models.Model):
    itemid = models.AutoField(primary_key=True)
    cartid = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    giftcardid = models.ForeignKey('giftcards.GiftCard', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return display(self.giftcard.card_name)


class PaymentMethod(models.Model):
    paymentmethodid = models.AutoField(primary_key=True)
    '''
    # Reference is in Payment class:
    paymentid = models.OneToOneField(Payment, on_delete=SET_NULL, null=True)
    '''
    name = models.CharField(max_length=50)
    description = models.TextField()
    cardnumber = models.CharField(max_length=20)
    expirationdate = models.DateTimeField()
    cvv = models.CharField(max_length=4)
    nameoncard = models.CharField(max_length=100)
    status = models.CharField(max_length=20)

    def __str__(self):
        return display(self.name)

    def validatePaymentMethod(self):
        pass


class Payment(models.Model):
    paymentid = models.AutoField(primary_key=True)
    paymentmethod = models.OneToOneField(PaymentMethod, on_delete=models.SET_NULL, null=True)
    userid = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    '''
    # Reference is in Order class:
    orderid = models.OneToOneField(Order, on_delete=models.CASCADE)
    '''
    amount = models.FloatField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return f'Payment({self.paymentid}, User({self.userid}):  {self.amount:,.2f})'

    def processPayment(self):
        pass


class OrderStatus(models.IntegerChoices):
    PENDING = 1
    PROCESSING = 2
    SHIPPED = 3
    COMPLETED = 4
    CANCELLED = 5


class Order(models.Model):
    orderid = models.AutoField(primary_key=True)
    userid = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    '''
    # Reference is in OrderItem class:
    itemid = models.ForeignKey(OrderItem, on_delete=CASCADE)
    '''
    orderdate = models.DateTimeField(auto_now_add=True)
    orderstatus = models.IntegerField(choices=OrderStatus, default=1)
    orderTotal = models.FloatField(default=0.0)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    recipient = models.OneToOneField(
        'accounts.CustomUser', on_delete=models.CASCADE, related_name='recipient'
    )

    def __str__(self):
        return f'Order({self.orderid}, User({self.userid}):  {self.orderTotal:,.2f})'

    def updateOrderTotal(self):
        pass


class OrderItem(models.Model):
    itemid = models.AutoField(primary_key=True)
    orderid = models.ForeignKey(Order, on_delete=models.CASCADE)
    giftcardid = models.ForeignKey('giftcards.GiftCard', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return display(self.giftcardid.card_name)
