from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    """Get value from dictionary by key, return None if not found."""
    if d is None:
        return None
    return d.get(key, None)

@register.filter
def list_get(l, index):
    """Get value from list by index, return None if not found."""
    if l is None or not isinstance(l, list):
        return None
    try:
        return l[index]
    except (IndexError, TypeError):
        return None