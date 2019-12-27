from django.shortcuts import render
from .forms import UserAddressForm
from .models import UserAddress
from django.contrib.auth.decorators import login_required


@login_required
def address_form(request):
    addresses = UserAddress.objects.filter(user=request.user)
    if request.method == 'POST':
        form = UserAddressForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = request.user
            new_address_obj = UserAddress(
                user=user,
                name=cd['name'],
                street_address=cd['street_address'],
                street_address_line2=cd['street_address_line2'],
                zipcode=cd['zipcode'],
                city=cd['city'],
                state=cd['state'],
                country=cd['country'],
            )
            new_address_obj.save()
    else:
        form = UserAddressForm()

    return render(request, 'address/address_form.html', {
        'page': 'address_form',
        'form': form,
        'addresses': addresses,
        })
