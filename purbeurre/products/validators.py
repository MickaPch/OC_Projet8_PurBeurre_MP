from django.core.exceptions import ValidationError


def validate_search_type(value):
    """Validate only types from list to prevent url input"""

    type_list = [
        'search',
        'brand',
        'category',
        'store'
    ]

    if value not in type_list:
        raise ValidationError('Type must be in {}.'.format(', '.join(type_list)))
