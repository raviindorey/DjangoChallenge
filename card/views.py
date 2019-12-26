from django.shortcuts import render


def card_list(request):
    return render(request, 'cards/card_list.html', {'page': 'cards'})
