from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Address

CustomUser = get_user_model()


class AddressAdmin(admin.ModelAdmin):
    model = Address


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        'email',
        'username',
        'role',
        'is_superuser'
    ]

    '''
    Attempt #1 - didn't work:
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ['role', 'shippingaddress']}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ['role', 'shippingaddress']}),)

    Attempt #2 - works, from Django Forum:
    https://forum.djangoproject.com/t/fielderror-unknown-field-s-usable-password-specified-for-customuser/36560
    * Have to exclude 'usable_password' or get FieldError when adding user
    * that this is an unknown field:
    '''
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'role', 'shippingaddress', 'password1', 'password2'),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Address, AddressAdmin)
