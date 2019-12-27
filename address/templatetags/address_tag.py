from django import template
register = template.Library()


@register.filter(name='address_cleaner')
def remove_nones_from_address(address_string):
    return address_string.replace('None', '')
