import requests
import os

from urllib.parse import urlencode

from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, View, FormView
from django.views.generic.base import ContextMixin
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt

from products.models import (
    Products,
    Categories,
    ProdCat,
    Brands,
    ProdBrand,
    Stores,
    ProdStore,
    UserSave
)
from products.forms import SearchForm, SaveForm, DeleteForm
from user.views import UserFormContext
from products.queries import GetProductsQueryTool, CheckProduct, UserProducts


class ProductFormContext(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(
            auto_id=False
        )
        return context


class SearchFormRedirect(View):
    """Search for products in database"""

    def post(self, request, **kwargs):

        search_form = SearchForm(
            request.POST,
            auto_id=False
        )

        if search_form.is_valid():
            search = search_form.cleaned_data['product_search']
            product = CheckProduct(search).check()
            if product is not None:
                return redirect(f'/products/product/{search}/')
            else:
                return redirect(f'/products/search/{search}/')
        else:
            return redirect('/')


class ProductsView(TemplateView, ProductFormContext, UserFormContext):
    """View to show searched products"""

    template_name = "products/search.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        search = kwargs['search']
        context['search_form'] = SearchForm(
            initial={'product_search': search},
            auto_id=False
        )

        context['search_type'] = 'search'
        context['products'] = GetProductsQueryTool(search).get_all_products()

        return context


class BrandView(ProductsView):
    """View to show searched products"""

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        brand = kwargs['search']

        context['search_type'] = 'brand'
        context['products'] = GetProductsQueryTool(brand).get_products_by_brand()

        return context


class CategoryView(ProductsView):
    """View to show searched products"""

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        category = kwargs['search']

        context['search_type'] = 'category'
        context['products'] = GetProductsQueryTool(category).get_products_by_category()

        return context


class StoreView(ProductsView):
    """View to show searched products"""

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        store = kwargs['search']

        context['search_type'] = 'store'
        context['products'] = GetProductsQueryTool(store).get_products_by_store()

        return context


class ProductView(TemplateView, ProductFormContext, UserFormContext):
    """View to show searched products"""

    template_name = "products/product.html"

    def get_context_data(self, **kwargs):


        context = super().get_context_data(**kwargs)
        product_code = kwargs['search']
        context['search_form'] = SearchForm(
            initial={'product_search': product_code},
            auto_id=False
        )

        product = CheckProduct(product_code)
        check_product = product.check()
        if check_product is not None:
            context['product'] = check_product
            context['brand'], context['brands'] = product.get_brands()
            context['stores'] = product.get_stores()
            context['categories'] = product.get_categories()
            context['alternatives'] = product.get_alternatives()

        if self.request.user.is_authenticated:
            user_products = UserProducts(self.request.user)
            context['user_products'] = user_products.get_user_products()

        return context


class MyProductsView(
    LoginRequiredMixin,
    TemplateView,
    ProductFormContext,
    UserFormContext
):
    """View to show searched products"""

    template_name = "products/my_products.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        user_products = UserProducts(self.request.user)
        context['products'] = user_products.get_user_products()

        return context


class SaveView(LoginRequiredMixin, FormView):
    """Save selected products"""

    template_name = "products/save.html"
    form_class = SaveForm
    success_url = "/products/my_products/"

    def form_valid(self, form):

        form.save_products(self.request.user)

        return super().form_valid(form)


class DeleteView(LoginRequiredMixin, FormView):
    """Delete selected products"""

    template_name = "products/delete.html"
    form_class = DeleteForm
    success_url = "/products/my_products/"

    def form_valid(self, form):

        form.delete_products(self.request.user)

        return super().form_valid(form)
