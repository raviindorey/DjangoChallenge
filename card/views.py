from django.shortcuts import render
from .forms import CardForm
from .models import Card


def card_list(request):
    print(request)
    cards = Card.objects.all()
    if request.method == 'POST':
        card_form = CardForm(data=request.POST)
        if card_form.is_valid():
            cd = card_form.cleaned_data
            print(cd)
            card_name = cd.get('card_name')
            card_number = cd.get('card_number')
            if card_name and card_number:
                Card.objects.create(
                    card_name=card_name,
                    card_number=card_number
                )
                return render(request, 'cards/card_list.html', {
                    'page': 'cards',
                    'cards': cards,
                    'card_form': card_form,
                })

    else:
        card_form = CardForm()

    return render(request, 'cards/card_list.html', {
        'page': 'cards',
        'cards': cards,
        'card_form': card_form,
    })
