from django import template
from card.utils import create_hyphen_string
register = template.Library()


@register.filter(name='card_number_hyphener')
def cards_number_to_number_hyphens(number_string):
    return create_hyphen_string(number_string)
