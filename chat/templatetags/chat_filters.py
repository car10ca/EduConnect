from django import template

register = template.Library()

@register.filter
def notin_list(value, list_str):
    """
    Custom template filter to check if the given value is not in a comma-separated list of items.
    Usage in template: {{ value|notin_list:"item1,item2,item3" }}
    """
    excluded_list = list_str.split(',')
    return value not in excluded_list
