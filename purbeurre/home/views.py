"""Application home views"""
from django.shortcuts import render

from .forms import ProductBarForm, ProductForm

def home(request):
    """Home page"""
    navbar_form = ProductBarForm()
    form = ProductForm()


    return render(request, 'home/home.html', locals())
