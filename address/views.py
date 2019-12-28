from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .forms import UserAddressForm
from .models import UserAddress


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

            new_address = new_address_obj.get_full_address()\
                .replace('None', '')

            # Allow force create
            if request.POST.get('request_type') != 'ajax':
                new_address_obj.save()

            else:
                """
                Save/Update in following conditions
                1. Save a new address
                2. Updated iff existing (current) address is subset of new
                   address.That is, a new information (field) was added.
                   We are not concerned about user removing/clearing/non-subset
                   fields, as it won't be a subset of current address
                3. Updated existing if no new field was added,
                   but existing was field modified
                """

                try:
                    current_address_obj = UserAddress.objects\
                                            .filter(user=user)\
                                            .latest('created')

                    changing_field = request.POST.get('changing_field')
                    changing_value = request.POST.get('changing_value')

                    if changing_value != "":
                        if getattr(current_address_obj, changing_field, None):
                            current_value = getattr(
                                current_address_obj,
                                changing_field
                                )
                            if current_value in changing_value:
                                setattr(
                                    current_address_obj,
                                    changing_field,
                                    changing_value
                                )
                                current_address_obj.save()
                                return JsonResponse({
                                    'status': 'updated',
                                    'name': new_address_obj.name,
                                    'address': new_address,
                                })
                        else:
                            new_address_obj.save()
                            return JsonResponse({
                                'status': 'created',
                                'name': new_address_obj.name,
                                'address': new_address,
                            })

                except UserAddress.DoesNotExist:
                    # First Address ever
                    new_address_obj.save()
                    return JsonResponse({
                        'status': 'created',
                        'name': new_address_obj.name,
                        'address': new_address,
                    })
        else:
            raise ValidationError("Invalid Data")

    else:
        try:
            form = UserAddressForm(instance=addresses.latest('created'))
        except UserAddress.DoesNotExist:
            form = UserAddressForm()
    return render(request, 'address/address_form.html', {
        'page': 'address_form',
        'form': form,
        'addresses': addresses
        })
