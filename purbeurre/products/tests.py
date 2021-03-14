from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.test import TestCase, RequestFactory, Client, LiveServerTestCase

from unittest.mock import patch

from products.apps import ProductsConfig
from products.models import (
    Products,
    Categories,
    Brands,
    Stores,
    ProdCat,
    ProdBrand,
    ProdStore,
    UserSave
)
from products.management.commands.classes import (
    ImportCategories,
    Category,
    ProductImportation
)
from user.models import User

import os


def initiate_test_db():
    User.objects.create(
        username="admin", 
        email="foo@example.com",
        password=make_password("admin")
    )
    Categories.objects.create(
        name='test',
        url='http://foo.example.com/category/test',
        name_fr='Test'
    )
    category_test = Categories.objects.get(name='test')
    new_product = Products.objects.create(
        code='123456789',
        name='Test product',
        url='http://foo.example.com/product/123456789',
        quantity='XX g',
        country='Test',
        ingredients='Tests',
        energy=123,
        fat=123,
        satured_fat=123,
        carbohydrates=123,
        sugar=123,
        fibers=123,
        proteins=123,
        salt=123,
        sodium=123,
        nutriscore='E',
        image_url='http://foo.example.com/product/123456789.jpg',
        compare_to_category=category_test
    )
    product_test = Products.objects.get(
        code='123456789'
    )
    ProdCat.objects.create(
        product=product_test,
        category=category_test
    )
    Brands.objects.create(
        name='Test'
    )
    brand_test = Brands.objects.get(name='Test')
    ProdBrand.objects.create(
        product=product_test,
        brand=brand_test
    )
    Stores.objects.create(
        name='Test'
    )
    store_test = Stores.objects.get(name='Test')
    ProdStore.objects.create(
        product=product_test,
        store=store_test
    )

class ProductsConfigTest(TestCase):
    """Testing products app"""

    def test_app_products(self):
        """Test app name"""
        self.assertEqual(
            ProductsConfig.name,
            'products'
        )
        self.assertEqual(
            apps.get_app_config('products').name,
            'products'
        )

class ProductsViewTest(LiveServerTestCase):
    """Testing products view"""
    fixtures = ['users.json', 'products.json']

    @patch('products.views.SearchForm.is_valid', spec=True)
    def test_get_products_invalid_search_form(self, MockSearchForm):
        MockSearchForm.return_value = False
        self.client.get(
            '/search/',
            {
                'product_search': 'test',
                'type': 'search'
            },
            follow=True
        )
        self.assertTemplateUsed('home.html')

    @patch('products.views.ProductView')
    @patch('products.views.SearchForm')
    def test_get_products_valid_search_form(self, MockSearchForm, MockProductView):
        MockSearchForm.is_valid.return_value = True
        MockProductView.get_product.return_value = None
        types = [
            'search',
            'brand',
            'store',
            'category'
        ]
        login_user = self.client.login(
            username='foo@example.com',
            password='admin'
        )
        self.assertEqual(login_user, True)
        for search_type in types:
            search_form = {
                'product_search': 'test',
                'type': search_type
            }
            MockSearchForm.return_value.cleaned_data = search_form
            self.client.get(
                '/search/',
                search_form,
                follow=True
            )
            self.assertTemplateUsed('search.html')

    @patch('products.views.ProductView')
    @patch('products.views.SearchForm')
    def test_get_products_redirect_product(self, MockSearchForm, MockProductView):
        MockSearchForm.is_valid.return_value = True
        MockProductView.get_product.return_value = 'test'
        MockSearchForm.return_value.cleaned_data = {
            'product_search': 'test',
            'type': 'search'
        }

        self.client.get(
            '/search/',
            {
                'product_search': 'test',
                'type': 'search'
            },
            follow=True
        )
        # Unexistant product --> redirect home
        self.assertTemplateUsed('home.html')


class ProductViewTest(TestCase):
    """Testing product view"""

    fixtures = ['users.json', 'products.json']

    def test_get_product(self):
        """Test get a product"""

        login_user = self.client.login(
            username='foo@example.com',
            password='admin'
        )
        self.assertEqual(login_user, True)

        self.client.get(
            '/product/',
            {
                'product_code': '3017620422003'
            },
            follow=True
        )
        self.assertTemplateUsed('product.html')

class SaveViewTest(TestCase):
    """"""
    def setUp(self):
        initiate_test_db()
        self.product_form = {
            'products_to_save': '123456789'
        }

    def test_save_product(self):
        self.client.login(
            username='foo@example.com',
            password='admin'
        )
        response = self.client.post(
            '/save/',
            self.product_form
        )
        user = User.objects.get(email='foo@example.com')
        product_saved = Products.objects.get(
            code='123456789'
        )
        save_count = UserSave.objects.filter(
            product=product_saved,
            user=user
        ).count()
        self.assertEqual(save_count, 1)
        self.assertEqual(response.status_code, 302)

    def test_actualize_save_date(self):
        self.client.login(
            username='foo@example.com',
            password='admin'
        )
        response = self.client.post(
            '/save/',
            self.product_form
        )
        user = User.objects.get(email='foo@example.com')
        product_saved = Products.objects.get(
            code='123456789'
        )
        save_count = UserSave.objects.filter(
            product=product_saved,
            user=user
        ).count()
        self.assertEqual(save_count, 1)
        self.assertEqual(response.status_code, 302)

        # Save again to actualize date
        response = self.client.post(
            '/save/',
            self.product_form
        )
        save_count = UserSave.objects.filter(
            product=product_saved,
            user=user
        ).count()
        self.assertEqual(save_count, 1)
        self.assertEqual(response.status_code, 302)

    def test_products_save_none(self):
        client = Client(
            HTTP_REFERER='/user/new/'
        )
        client.login(
            username='foo@example.com',
            password='admin'
        )
        response = client.post(
            '/save/',
            {'products_to_save': 'wrong_product_code'}
        )
        user = User.objects.get(email='foo@example.com')
        save_count = UserSave.objects.filter(
            user=user
        ).count()
        self.assertEqual(save_count, 0)
        self.assertEqual(response.status_code, 302)


class DeleteViewTest(TestCase):
    """"""
    def setUp(self):
        initiate_test_db()
        self.save_product_form = {
            'products_to_save': '123456789'
        }
        self.delete_product_form = {
            'products_to_delete': '123456789'
        }
        self.client.login(
            username='foo@example.com',
            password='admin'
        )
        self.client.post(
            '/save/',
            self.save_product_form
        )
        self.user = User.objects.get(email='foo@example.com')
        self.product_saved = Products.objects.get(
            code='123456789'
        )

    def test_delete_product(self):
        save_count = UserSave.objects.filter(
            product=self.product_saved,
            user=self.user
        ).count()
        self.assertEqual(save_count, 1)
        response = self.client.post(
            '/delete/',
            self.delete_product_form
        )
        save_count = UserSave.objects.filter(
            product=self.product_saved,
            user=self.user
        ).count()
        self.assertEqual(save_count, 0)
        self.assertEqual(response.status_code, 302)

    def test_products_delete_none(self):
        client = Client(
            HTTP_REFERER='/user/new/'
        )
        client.login(
            username='foo@example.com',
            password='admin'
        )
        response = client.post(
            '/delete/',
            {'products_to_delete': 'wrong_product_code'}
        )
        self.assertEqual(response.status_code, 302)

class UserProductsViewTest(TestCase):
    """"""
    def setUp(self):
        initiate_test_db()
        self.client.login(
            username='foo@example.com',
            password='admin'
        )

    def test_my_products_view(self):
        response = self.client.get(
            '/my_products/'
        )
        self.assertEqual(response.status_code, 200)

class ImportTest(TestCase):

    @patch('products.management.commands.classes.requests')
    def test_mock_import_categories(self, mock_requests):
        mock_requests.get.assert_not_called()
        ImportCategories()
        mock_requests.get.assert_called_once()

    @patch('products.models.Categories')
    @patch('products.management.commands.classes.requests')
    def test_mock_category_get_products(self, mock_requests, mock_category):
        mock_requests.get.assert_not_called()
        category = Category(mock_category)
        category.get_products_list()
        mock_requests.get.assert_called_once()
