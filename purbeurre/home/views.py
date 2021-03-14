"""Module home.views"""
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from user.views import UserFormView
from products.views import ProductFormView


class HomeView(ProductFormView, UserFormView):
    """View to show searched products"""

    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LegalNoticeView(ProductFormView, UserFormView):

    template_name = 'home/legal_notice.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
