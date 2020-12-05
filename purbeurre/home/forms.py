"""Homepage forms"""
from django import forms

class ProductBarForm(forms.Form):
    """Product search form"""
    bar_search = forms.CharField(
        max_length=100
    )

    bar_search.widget.attrs.update(
        {
            'class': 'form-control navbar-product-form',
            'placeholder': 'Chercher un produit'
        }
    )

class ProductForm(forms.Form):
    """Product search form"""
    product_search = forms.CharField(
        max_length=100
    )

    product_search.widget.attrs.update(
        {
            'class': 'form-control input-search-product',
            'placeholder': 'Chercher un produit'
        }
    )