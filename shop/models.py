from django.db import models


class ShoppingCart(models.Model):
    cartid = models.AutoField(primary_key=True)
    userid = models.OneToOneField(
        # Note:  on_delete=CASCADE is more like composition than aggregation:
        'accounts.CustomUser', on_delete=models.CASCADE, blank=True, null=True
    )
    orderTotal = models.FloatField(default=0.0)

    # Session management handled by Django - don't need where requiring current
    # user (accounts.CustomUser)

    def __str__(self):
        return f'{self.userid}({self.cartid})'


class ShoppingCartItem(models.Model):
    itemid = models.AutoField(primary_key=True)
    cartid = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    giftcardid = models.ForeignKey('giftcards.GiftCard', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return (
            self.giftcard.card_name[:30]
            if len(self.giftcard.card_name) <= 30
            else f'{self.giftcard.card_name[:27]}...'
        )


class PaymentMethod(models.Model):
    paymentmethodid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    cardnumber = models.CharField(max_length=20)
    expirationdate = models.DateTimeField()
    cvv = models.CharField(max_length=4)
    nameoncard = models.CharField(max_length=100)
    status = models.CharField(max_length=20)


class Payment(models.Model):
    paymentid = models.AutoField(primary_key=True)
    paymentmethod = models.OneToOneField(
        PaymentMethod, on_delete=models.SET_NULL, null=True
    )
    amount = models.FloatField()
    status = models.CharField(max_length=20)
    userid = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)


class Order(models.Model):
    orderid = models.AutoField(primary_key=True)
    orderdate = models.DateTimeField(auto_now_add=True)

    class OrderStatus(models.IntegerChoices):
        PENDING = 1
        PROCESSING = 2
        SHIPPED = 3
        COMPLETED = 4

    orderstatus = models.IntegerField(choices=OrderStatus, default=1)
    userid = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    totalamount = models.FloatField(default=0.0)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    recipient = models.OneToOneField(
        'accounts.CustomUser', on_delete=models.CASCADE, related_name='recipient'
    )


class OrderItem(models.Model):
    itemid = models.AutoField(primary_key=True)
    orderid = models.ForeignKey(Order, on_delete=models.CASCADE)
    giftcardid = models.ForeignKey('giftcards.GiftCard', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return (
            self.giftcard.card_name[:30]
            if len(self.giftcard.card_name) <= 30
            else f'{self.giftcard.card_name[:27]}...'
        )
