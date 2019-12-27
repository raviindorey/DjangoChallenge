from django.shortcuts import render
from django.views.decorators.debug import sensitive_post_parameters
from django.views.debug import SafeExceptionReporterFilter
from django.core.exceptions import ValidationError
from .forms import CardForm
from .models import Card
from .utils import create_hyphen_string


class CustomExceptionReporterFilter(SafeExceptionReporterFilter):
    def get_post_parameters(self, request):
        """
        Replace the values of POST parameter card_number
        Customized value for card number.
        https://docs.djangoproject.com/en/2.2/howto/error-reporting/#django.views.debug.SafeExceptionReporterFilter.get_post_parameters
        """
        if request is None:
            return {}
        else:
            sensitive_post_parameters = getattr(
                request,
                'sensitive_post_parameters',
                []
            )
            if self.is_active(request) and sensitive_post_parameters:
                cleansed = request.POST.copy()
                # Cleanse only the specified parameters.
                for param in sensitive_post_parameters:
                    if param in cleansed:
                        cleansed[param] = create_hyphen_string(cleansed[param])
                return cleansed
            else:
                return request.POST


@sensitive_post_parameters('card_number')
def card_list(request):
    request.exception_reporter_filter = CustomExceptionReporterFilter()
    cards = Card.objects.all()
    if request.method == 'POST':
        card_form = CardForm(data=request.POST)
        if card_form.is_valid():
            cd = card_form.cleaned_data
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
            raise ValidationError("Invalid Data")
    else:
        card_form = CardForm()

    return render(request, 'cards/card_list.html', {
        'page': 'cards',
        'cards': cards,
        'card_form': card_form,
    })
