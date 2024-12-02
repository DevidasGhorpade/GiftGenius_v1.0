from django.contrib import admin
from .models import GiftCardType, DigitalGiftCard, PhysicalGiftCard

admin.site.register(GiftCardType)
admin.site.register(DigitalGiftCard)
admin.site.register(PhysicalGiftCard)
