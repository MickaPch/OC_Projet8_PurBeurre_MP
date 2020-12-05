"""Application home views"""
from django.shortcuts import render

from .forms import ProductBarForm, ProductForm
from user.forms import ConnectionForm

def home(request):
    """Home page"""
    navbar_form = ProductBarForm()
    form = ProductForm()
    form_user = ConnectionForm()

    return render(request, 'home/home.html', locals())
