from django.contrib import admin

from .models import ShoppingCart, ShoppingCartItem, Payment, PaymentMethod, Order, OrderItem


class ShoppingCartAdmin(admin.ModelAdmin):
    model = ShoppingCart


class ShoppingCartItemAdmin(admin.ModelAdmin):
    model = ShoppingCartItem


class PaymentAdmin(admin.ModelAdmin):
    model = Payment


class PaymentMethodAdmin(admin.ModelAdmin):
    model = PaymentMethod


class OrderAdmin(admin.ModelAdmin):
    model = Order


class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem


admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(ShoppingCartItem, ShoppingCartItemAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(PaymentMethod, PaymentMethodAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
