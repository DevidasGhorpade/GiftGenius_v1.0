from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from giftcards.models import GiftCardType
from django.shortcuts import render, redirect
from shop.models import ShoppingCart
from django.contrib import messages
from django.views.generic import TemplateView


class ShopPageView(TemplateView):
    template_name = 'shop/shop.html'
    
def add_to_cart(request, giftcard_id):
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        giftcard = get_object_or_404(GiftCardType, card_type_id=giftcard_id)

        cart, created = ShoppingCart.objects.get_or_create(user_id=request.user)
        try:
            cart.add_item(giftcard, quantity)
            messages.success(request, f"{giftcard.card_name} added to cart.")
        except ValueError as e:
            messages.error(request, str(e))

    return redirect('cart_summary')

def cart_summary(request):
    cart = ShoppingCart.objects.filter(user_id=request.user).first()
    return render(request, 'shop/shop.html', {'cart': cart})

def remove_from_cart(request, giftcard_id):
    cart = ShoppingCart.objects.filter(user_id=request.user).first()
    if cart:
        giftcard = get_object_or_404(GiftCardType, card_type_id=giftcard_id)
        cart.remove_item(giftcard)
        messages.success(request, f"{giftcard.card_name} removed from cart.")
    return redirect('cart_summary')

def checkout(request):
    return render(request,'shop/order_summary.html')
