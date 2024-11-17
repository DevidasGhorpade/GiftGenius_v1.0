from django.db import models
from datetime import datetime

class GiftCard(models.Model):
    card_id = models.AutoField(primary_key=True)
    card_name = models.CharField(max_length=100)
    card_description = models.TextField()
    card_category = models.CharField(max_length=50)
    card_type = models.CharField(max_length=20)    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    card_status = models.CharField(max_length=20)
    expiration_date = models.DateField()
    card_number = models.CharField(max_length=50, unique=True)
    card_quantity = models.IntegerField()
    image_url = models.URLField(max_length=500, blank=True, null=True)
    
    def activate(self):
        self.card_status = "ACTIVE"
        self.save()

    def deactivate(self):
        self.card_status = "INACTIVE"
        self.save()

    def redeem(self, amount):
        if self.balance >= amount and self.card_status == "ACTIVE":
            self.balance -= amount
            self.save()
            return True
        return False

    def check_balance(self):
        return self.balance

    def check_availability(self):
        return self.card_status == "ACTIVE" and self.balance > 0