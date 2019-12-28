from django import forms
from .models import UserAddress


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        exclude = ('user', 'full_address')
