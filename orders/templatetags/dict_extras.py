from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    """Get value from dictionary by key, return '0' if not found."""
    if d is None:
        return '0'
    return d.get(key, '0')

@register.filter
def list_get(l, index):
    """Get value from list by index, return '0' if not found."""
    if l is None or not isinstance(l, list):
        return '0'
    try:
        return l[index]
    except (IndexError, TypeError):
        return '0'