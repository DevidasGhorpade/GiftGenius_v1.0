from django.db import models
from datetime import datetime

class GiftCardType(models.Model):
    card_id = models.AutoField(primary_key=True)
    card_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    card_description = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('BIRTHDAY', 'Birthday'),
        ('TRAVEL', 'Travel'),
        ('CLOTHING', 'Clothing'),
        ('BOOKS','Books'),
        ('RETAIL','Retail'),
        ('ENTERTAINMENT','Entertainment')
    ])
    type = models.CharField(max_length=20, choices=[
        ('PHYSICAL', 'Physical'),
        ('DIGITAL', 'Digital')
    ])
    quantity = models.PositiveIntegerField()
    gift_card_image_url = models.URLField(max_length=500, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.card_name


class GiftCard(models.Model):
    card_id = models.ForeignKey(GiftCardType, on_delete=models.CASCADE, related_name='gift_cards')
    card_number = models.CharField(max_length=50, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateField()
    cvv_number = models.CharField(max_length=10)
    gift_card_status = models.CharField(max_length=20, choices=[
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('EXPIRED', 'Expired'),
    ])

    def activate(self):
        if self.gift_card_status != 'EXPIRED':
            self.gift_card_status = "ACTIVE"
            self.save()

    def deactivate(self):
        self.gift_card_status = "INACTIVE"
        self.save()

    def __str__(self):
        return f"{self.card_number} - {self.gift_card_status}"
