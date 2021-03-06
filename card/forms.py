from django import forms
from .models import Card


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ('card_name', 'card_number',)
