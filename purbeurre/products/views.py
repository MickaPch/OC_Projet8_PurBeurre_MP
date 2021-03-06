import requests
import os

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
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
from products.forms import SearchForm, ProductForm
from user.forms import ConnectionForm


class ProductsView(TemplateView):
    """View to show searched products"""

    template_name = "/"

    @csrf_exempt
    def get(self, request, **kwargs):

        search_form = SearchForm(
            request.GET,
            auto_id=False
        )
        product_form = ProductForm(auto_id=False)
        form_user = ConnectionForm()

        if search_form.is_valid():
            search = search_form.cleaned_data['product_search']
            search_type = search_form.cleaned_data['type']
            product = ProductView.get_product(self, search)
            if search_type in ['search', 'product']:
                if (
                    product is not None
                    or search_type == 'product'
                ):
                    # Redirect to ProductView
                    get_product = "".join([
                        'http://',
                        request.META['HTTP_HOST'].strip(),
                        '/product/'
                    ])
                    url_product = requests.get(
                        get_product,
                        params={
                            'product_code': search
                        }
                    ).url

                    return redirect(url_product)
                else:
                    products_by_category = self.get_products_by_category(search)
                    products_by_brand = self.get_products_by_brand(search)
                    products_by_store = self.get_products_by_store(search)
                    products_by_name = self.get_products_by_name(search)
                    products = products_by_name.union(
                        products_by_category,
                        products_by_brand,
                        products_by_store
                    ).distinct()
            elif search_type == 'brand':
                products = self.get_products_by_brand(search)
            elif search_type == 'category':
                products = self.get_products_by_category(search)
            elif search_type == 'store':
                products = self.get_products_by_store(search)

            if request.user.is_authenticated:
                user_products = MyProductsView.get_user_products(self, request.user)

            return render(request, 'products/search.html', locals())

        else:
            return redirect('/')

    def get_products_by_brand(self, search):
        """Return products find by brand"""
        prodbrand_results = ProdBrand.objects.filter(
            brand__name__icontains=search
        )
        products = Products.objects.filter(
            prodbrand__in=prodbrand_results
        ).distinct()

        return products

    def get_products_by_category(self, search):
        """Return products find by category"""
        prodcat_results = ProdCat.objects.filter(
            Q(category__name__icontains=search)
            | Q(category__name_fr__icontains=search)
        )
        products = Products.objects.filter(
            prodcat__in=prodcat_results
        ).distinct()

        return products

    def get_products_by_store(self, search):
        """Return products find by store"""
        prodstore_results = ProdStore.objects.filter(
            store__name__icontains=search
        )
        products = Products.objects.filter(
            prodstore__in=prodstore_results
        ).distinct()

        return products

    def get_products_by_name(self, search):
        """Return products find by name"""
        
        products = Products.objects.filter(
            name__icontains=search
        ).distinct()

        return products


class ProductView(TemplateView):
    """View to show searched products"""

    template_name = "/"
    
    @csrf_exempt
    def get(self, request, **kwargs):

        product_form = ProductForm(
            request.GET,
            auto_id=False
        )
        search_form = SearchForm(auto_id=False)
        form_user = ConnectionForm()

        if product_form.is_valid():
            code = product_form.cleaned_data['product_code']
            product = self.get_product(code)
            if product is not None:
                brand, brands = self.get_brands(product)
                stores = self.get_stores(product)
                categories = self.get_categories(product)
                alternatives = self.get_alternatives(product)

                if request.user.is_authenticated:
                    user_products = MyProductsView.get_user_products(self, request.user)

                return render(request, 'products/product.html', locals())

    def get_product(self, code):
        """
        Check if registered product
        """
        try:
            product = Products.objects.get(
                code=code
            )
        except Products.DoesNotExist:
            product = None
        
        return product

    def get_brands(self, product):
        """Return main and list of all brands of a product"""

        prodbrand_results = ProdBrand.objects.filter(
            product__code=product.code
        )
        brands = [brand.brand.name for brand in prodbrand_results]
        brand = prodbrand_results[0].brand.name

        return brand, brands

    def get_stores(self, product):
        """Return list of all stores of a product"""

        prodstore_results = ProdStore.objects.filter(
            product__code=product.code
        )
        stores = [store.store.name for store in prodstore_results]

        return stores

    def get_categories(self, product):
        """Return list of all categories of a product"""
        
        prodcategory_results = ProdCat.objects.filter(
            product__code=product.code
        ).exclude(
            category__name=product.compare_to_category.name
        )
        categories = [category.category.name_fr for category in prodcategory_results]

        return categories


    def get_alternatives(self, product):
        """Return alternatives of a product and redirect to product page"""

        alternatives = Products.objects.filter(
            compare_to_category=product.compare_to_category,
            nutriscore__lte=product.nutriscore
        ).exclude(
            code=product.code
        ).distinct().order_by('nutriscore')

        return alternatives

class SaveView(LoginRequiredMixin,TemplateView):
    """Save selected products"""

    template_name = "/"

    def post(self, request, **kwargs):

        products_to_save = request.POST['products_to_save']
        search_form = SearchForm(auto_id=False)
        form_user = ConnectionForm()

        try:
            new_products = products_to_save.split(',')
            for product_code in new_products:
                product_object = Products.objects.get(
                    code=product_code
                )
                product, new_product = UserSave.objects.get_or_create(
                    user=request.user,
                    product=product_object
                )
                if not new_product:
                    product.save()
            return redirect('my_products')
        except:
            return redirect(request.META.get('HTTP_REFERER'))

class DeleteView(LoginRequiredMixin,TemplateView):
    """Delete selected products"""

    template_name = "/"

    def post(self, request, **kwargs):

        products_to_delete = request.POST['products_to_delete']
        search_form = SearchForm(auto_id=False)
        form_user = ConnectionForm()

        try:
            new_products = products_to_delete.split(',')
            for product_code in new_products:
                product_object = Products.objects.get(
                    code=product_code
                )
                UserSave.objects.filter(
                    user=request.user,
                    product=product_object
                ).delete()
            return redirect('my_products')
        except:
            return redirect(request.META.get('HTTP_REFERER'))

class MyProductsView(LoginRequiredMixin, TemplateView):
    """View to show searched products"""

    template_name = "/"

    def get(self, request, **kwargs):

        product_form = ProductForm(
            request.GET,
            auto_id=False
        )
        search_form = SearchForm(auto_id=False)
        form_user = ConnectionForm()
        products = self.get_user_products(request.user)

        return render(request, 'products/my_products.html', locals())

    def get_user_products(self, user):
        """Return user registered products"""

        user_products = UserSave.objects.filter(
            user=user
        )
        products = Products.objects.filter(
            usersave__in=user_products
        ).distinct().order_by('nutriscore')

        return products
