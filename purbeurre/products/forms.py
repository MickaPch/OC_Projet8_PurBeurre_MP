"""Homepage forms"""
from django import forms

from products.models import (
    Products,
    ProdBrand
)
from products import validators

class SearchForm(forms.Form):
    """Product search form"""
    product_search = forms.CharField(
        max_length=100
    )
    type = forms.CharField(
        max_length=100,
        initial='search',
        validators=[validators.validate_search_type]
    )

    product_search.widget.attrs.update(
        {
            'class': 'form-control input-search-product',
            'placeholder': 'Chercher un produit'
        }
    )
    type.widget.attrs.update(
        {
            'class': 'input-type'
        }
    )

class ProductForm(forms.Form):
    """Product form"""

    product_code = forms.CharField(
        max_length=100
    )
