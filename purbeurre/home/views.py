"""Module home.views"""
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from user.forms import ConnectionForm
from products.forms import SearchForm


class HomeView(TemplateView):
    """View to show searched products"""

    template_name = "/"

    @csrf_exempt
    def get(self, request, **kwargs):
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


def legal_notice(request):
    """Legal Notice"""
    search_form = SearchForm(
        auto_id=False,
        initial={
            'product_search': "",
            'type': 'search'
        }
    )
    form_user = ConnectionForm()

    return render(request, 'home/legal_notice.html', locals())
