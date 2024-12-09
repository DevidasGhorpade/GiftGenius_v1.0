from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

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
        'address',
        'is_superuser'
    ]
    # Can't use this - results in error:
    # fields =  ['username', 'email', 'role', 'address', 'shipping_address', 'password1', 'password2']

    '''
    Attempt #1 - didn't work:
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ['role', 'shippingaddress']}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ['role', 'shippingaddress']}),)

    Attempt #2 - works, from Django Forum:
    https://forum.djangoproject.com/t/fielderror-unknown-field-s-usable-password-specified-for-customuser/36560
    * Have to exclude 'usable_password' or get FieldError when adding user
    * that this is an unknown field:
    '''
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'email', 'preferred_category', 'role', 'shipping_address'
            )}
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'preferred_category', 'role', 'shipping_address',
                'password1', 'password2'
                ),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Address, AddressAdmin)
