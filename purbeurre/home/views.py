"""Application home views"""
from django.shortcuts import render

from user.forms import ConnectionForm
from products.forms import SearchForm


def home(request):
    """Home page"""
    search_form = SearchForm(
        auto_id=False,
        initial={
            'product_search': "",
            'type': 'search'
        }
    )
    form_user = ConnectionForm()

    return render(request, 'home/home.html', locals())
