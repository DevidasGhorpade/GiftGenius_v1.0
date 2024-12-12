from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class GiftRecipientForm(forms.Form):
    giver_name = forms.CharField(
        label="Your/Giver's Name",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Enter your name"}),
    )
    recipient_name = forms.CharField(
        label="Recipient's Name",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Enter recipient's name"}),
    )
    recipient_email = forms.EmailField(
        label="Recipient's Email",
        widget=forms.EmailInput(attrs={"placeholder": "Enter recipient's email"}),
    )
    recipient_address1 = forms.CharField(
        label="Recipient's Shipping Address Line 1",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Enter recipient's address line 1"}),
    )
    recipient_address2 = forms.CharField(
        label="Recipient's Shipping Address Line 2",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Enter recipient's address line 2"}),
    )
    recipient_city = forms.CharField(
        label="Recipient's City",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Enter recipient's city"}),
    )
    recipient_state = forms.CharField(
        label="Recipient's State",
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "Enter recipient's state"}),
    )
    recipient_zip = forms.CharField(
        label="Recipient's Zip Code",
        max_length=10,
        widget=forms.TextInput(attrs={"placeholder": "Enter recipient's zip code"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            "giver_name",
            "recipient_name",
            "recipient_email",
            "recipient_address1",
            "recipient_address2",
            "recipient_city",
            "recipient_state",
            "recipient_zip",
        )


class PaymentForm(forms.Form):
    card_number = forms.CharField(
        label="Card Number",
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "Enter card number"}),
    )
    cvv = forms.CharField(
        label="CVV", max_length=4, widget=forms.TextInput(attrs={"placeholder": "Enter CVV"})
    )
    expiration_date = forms.DateField(
        label="Expiration Date",
        widget=forms.DateInput(attrs={"placeholder": "Enter expiration date"}),
    )
    card_holder_name = forms.CharField(
        label="Name on Card",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Enter name on card"}),
    )
    card_holder_address1 = forms.CharField(
        label="Card Holder's Address Line 1",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Enter card holder's address line 1"}),
    )
    card_holder_address2 = forms.CharField(
        label="Card Holder's Address Line 2",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Enter card holder's address line 2"}),
    )
    card_holder_city = forms.CharField(
        label="Card Holder's City",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Enter card holder's city"}),
    )
    card_holder_state = forms.CharField(
        label="Card Holder's State",
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "Enter card holder's state"}),
    )
    card_holder_zip = forms.CharField(
        label="Card Holder's Zip Code",
        max_length=10,
        widget=forms.TextInput(attrs={"placeholder": "Enter card holder's zip code"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            "card_number",
            "cvv",
            "expiration_date",
            "card_holder_name",
            "card_holder_address1",
            "card_holder_address2",
            "card_holder_city",
            "card_holder_state",
            "card_holder_zip",
        )
