from django.shortcuts import render


def address_form(request):
    return render(request, 'address/address_form.html', {
        'page': 'address_form',
        })
