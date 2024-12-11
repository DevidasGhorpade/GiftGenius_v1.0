from datetime import datetime
import secrets

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView

from .forms import GiftRecipientForm, PaymentForm
from .models import Order, OrderItem, Payment, PaymentMethod, ShoppingCart
from accounts.models import Address, CustomUser
from giftcards.models import GiftCardType


class ShopPageView(TemplateView):
    template_name = 'shop/shop.html'

def add_to_cart(request, giftcard_id):
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        giftcard = get_object_or_404(GiftCardType, card_type_id=giftcard_id)

        cart, created = ShoppingCart.objects.get_or_create(user=request.user)
        try:
            cart.add_item(giftcard, quantity)
            messages.success(request, f"{giftcard.card_name} added to cart.")
        except ValueError as e:
            messages.error(request, str(e))

    return redirect('cart_summary')

def cart_summary(request):
    cart = ShoppingCart.objects.filter(user=request.user).first()
    return render(request, 'shop/shop.html', {'cart': cart})

def remove_from_cart(request, giftcard_id):
    if cart := ShoppingCart.objects.filter(user=request.user).first():
        giftcard = get_object_or_404(GiftCardType, card_type_id=giftcard_id)
        cart.remove_item(giftcard)
        messages.success(request, f"{giftcard.card_name} removed from cart.")
    return redirect('cart_summary')

def order_summary(request):
    return render(request,'shop/order_summary.html')

def create_or_get_address(address):
    # Existing?
    if not (address_exists := Address.objects.filter(
        street_address1=address.street_address1, street_address2=address.street_address2,
        city=address.city, state=address.state, zip_code=address.zip_code
    ).first()):
        address.save()
    else:
        address = address_exists

    return address

def gift_recipient(request):
    if request.method == 'POST':
        form = GiftRecipientForm(request.POST)
        if form.is_valid():
            # Process the data and update database
            address = Address()

            address.street_address1 = form.cleaned_data['recipient_address1']
            address.street_address2 = form.cleaned_data['recipient_address2']
            address.city = form.cleaned_data['recipient_city']
            address.state = form.cleaned_data['recipient_state']
            address.zip_code = form.cleaned_data['recipient_zip']
            address.address_type = 1

            address = create_or_get_address(address)

            user = CustomUser()

            # Existing?
            username = form.cleaned_data['recipient_email'].split('@')[0]
            if not (user := CustomUser.objects.filter(username=username).first()):
                user = CustomUser()
                user.username = form.cleaned_data['recipient_email'].split('@')[0]
                user.password = secrets.token_urlsafe(50)

            user.first_name = form.cleaned_data['recipient_name'].split()[0]
            user.last_name = ' '.join(form.cleaned_data['recipient_name'].split()[1:])
            user.email = form.cleaned_data['recipient_email']
            user.role = 3
            user.address = address
            user.save()

            # Store in session
            request.session['recipient'] = user.id
            return redirect('gift_payment')
    else:
        form = GiftRecipientForm()
    return render(request, 'shop/recipient.html', {'form': form})

def gift_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Process the data and update database
            card = PaymentMethod()
            card.name = f"{form.cleaned_data['card_holder_name']} Credit Card"
            card.card_number = form.cleaned_data['card_number']
            card.expiration_date = form.cleaned_data['expiration_date']
            card.cvv = form.cleaned_data['cvv']
            card.card_holder_name = form.cleaned_data['card_holder_name']

            address = Address()
            address.street_address1 = form.cleaned_data['card_holder_address1']
            address.street_address2 = form.cleaned_data['card_holder_address2']
            address.city = form.cleaned_data['card_holder_city']
            address.state = form.cleaned_data['card_holder_state']
            address.zip_code = form.cleaned_data['card_holder_zip']
            address.address_type = 1

            address = create_or_get_address(address)

            card.card_holder_address = address
            card.save()

            # Store in session
            request.session['payment_method'] = card.payment_method_id
            return redirect('review_order')
    else:
        form = PaymentForm()
    return render(request, 'shop/payment.html', {'form': form})

def review_order(request):
    cart = ShoppingCart.objects.filter(user=request.user).first()
    recipient = CustomUser.objects.get(id=request.session['recipient'])
    card = PaymentMethod.objects.get(payment_method_id=request.session['payment_method'])
    card.card_number = card.card_number[-4:]

    if request.method == 'POST':
        '''
        Options:
        1) Purchase
            * Create/record transaction
            * Remove items from cart
            * Remove/deduct items from inventory
            * Display Order Summary page
            Bonus:  See if can show digital/plastic delivery
        2) Cancel

        Either way, then return to Gift Cards page
        '''
        action = request.POST.get('action')  # Get the value of the pressed button

        if action == 'purchase':
            payment = Payment()
            payment.payment_method = PaymentMethod.objects.get(
                payment_method_id=request.session['payment_method']
            )
            payment.user = request.user
            payment.amount = cart.order_total
            payment.save()

            order = Order()
            order.user = request.user
            order.order_date = datetime.now()
            order.order_status = 1
            order.order_total = cart.order_total
            order.payment = payment
            order.recipient = recipient
            order.save()

            for item in cart.get_items():
                '''
                # Future:
                order_item = OrderItem()
                order_item.order = order

                # Create correct gift card type:
                order_item.card = ...
                order_item.quantity = item.quantity
                order_item.save()
                '''

                # Update inventory:
                item.card_type.card_quantity -= item.quantity
                item.card_type.save()

            cart.clear_cart()
            cart.save()

            return render(request, 'shop/order_summary.html', {'order': order})

        # Do nothing if cancel selected:
        # action == 'cancel':

        return redirect('giftcard_list')


    return render(request, 'shop/review_order.html', {
        'cart': cart, 'recipient': recipient, 'card': card
    })
