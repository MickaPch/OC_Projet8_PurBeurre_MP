"""Tests for products app views"""
from django.test import TestCase

from unittest.mock import patch

from products.views import ProductFormContext


class ProductFormTest(TestCase):
    """Testing product form view"""

    def setUp(self):
        self.product_form = {'product_search': 'some_product'}

    @patch('products.views.SearchForm')
    def test_search_form(self, MockSearchForm):
        attrs = {
            'return_value.is_valid.return_value': True,
            'return_value.cleaned_data': self.product_form
        }
        MockSearchForm.configure_mock(**attrs)
        context_object = ProductFormContext()
        response = context_object.get_context_data()
        MockSearchForm.assert_called()
        self.assertIn(
            'search_form',
            response
        )

class ProductFormRedirectTest(TestCase):
    """Testing products form redirect to views"""

    def setUp(self):
        self.product = 'some_product'

    @patch('products.views.SearchForm')
    def test_search_product_form_success(self, MockSearchForm):
        product_form = {'product_search': self.product}
        attrs = {
            'return_value.is_valid.return_value': True,
            'return_value.cleaned_data': product_form
        }
        MockSearchForm.configure_mock(**attrs)
        response = self.client.post(
            '/products/search',
            product_form
        )
        MockSearchForm.assert_called()
        self.assertRedirects(
            response,
            f'/products/search/{self.product}/',
            fetch_redirect_response=False
        )

    @patch('products.views.SearchForm')
    def test_search_product_form_redirect_homepage(self, MockSearchForm):
        product_form = {'product_search': self.product}
        attrs = {
            'return_value.is_valid.return_value': False,
            'return_value.cleaned_data': product_form
        }
        MockSearchForm.configure_mock(**attrs)
        response = self.client.post(
            '/products/search',
            product_form
        )
        MockSearchForm.assert_called()
        self.assertRedirects(
            response,
            '/',
            fetch_redirect_response=False
        )

    @patch('products.views.CheckProduct')
    @patch('products.views.SearchForm')
    def test_search_product_form_redirect_product(self, MockSearchForm, MockCheckProduct):
        product_form = {'product_search': self.product}
        attrs = {
            'return_value.is_valid.return_value': True,
            'return_value.cleaned_data': product_form
        }
        MockSearchForm.configure_mock(**attrs)
        MockCheckProduct.return_value.check.return_value = object()
        response = self.client.post(
            '/products/search',
            product_form
        )
        MockSearchForm.assert_called()
        self.assertRedirects(
            response,
            f'/products/product/{self.product}/',
            fetch_redirect_response=False
        )


class ProductsViewTest(TestCase):
    """Testing products view"""

    def setUp(self):
        self.product = 'some_product'

    def test_search_products_good_template(self):
        self.client.get(f'/products/search/{self.product}')

        self.assertTemplateUsed('products/search.html')
        
    def test_search_products_good_context(self):
        response = self.client.get(f'/products/search/{self.product}/')
        self.assertIn(
            'search_type',
            response.context
        )
        self.assertEqual(
            'search',
            response.context['search_type']
        )


class BrandViewTest(TestCase):
    """Testing brand view"""

    def setUp(self):
        self.product = 'some_brand'

    def test_search_products_good_template(self):
        self.client.get(f'/products/brand/{self.product}')

        self.assertTemplateUsed('products/search.html')
        
    def test_search_products_good_context(self):
        response = self.client.get(f'/products/brand/{self.product}/')
        self.assertIn(
            'search_type',
            response.context
        )
        self.assertEqual(
            'brand',
            response.context['search_type']
        )


class CategoryViewTest(TestCase):
    """Testing category view"""

    def setUp(self):
        self.product = 'some_category'

    def test_search_products_good_template(self):
        self.client.get(f'/products/category/{self.product}')

        self.assertTemplateUsed('products/search.html')
        
    def test_search_products_good_context(self):
        response = self.client.get(f'/products/category/{self.product}/')
        self.assertIn(
            'search_type',
            response.context
        )
        self.assertEqual(
            'category',
            response.context['search_type']
        )


class StoreViewTest(TestCase):
    """Testing store view"""

    def setUp(self):
        self.product = 'some_store'

    def test_search_products_good_template(self):
        self.client.get(f'/products/store/{self.product}')

        self.assertTemplateUsed('products/search.html')
        
    def test_search_products_good_context(self):
        response = self.client.get(f'/products/store/{self.product}/')
        self.assertIn(
            'search_type',
            response.context
        )
        self.assertEqual(
            'store',
            response.context['search_type']
        )


class ProductViewTest(TestCase):
    """Testing product view"""

    fixtures = ['users.json']

    def setUp(self):
        self.code = 'some_product'
        self.user = {
            'username': 'foo@example.com',
            'password': 'admin'
        }
        self.attrs = {
            'return_value.check.return_value': object(),
            'return_value.get_brands.return_value': [str(), list()],
            'return_value.get_stores.return_value': list(),
            'return_value.get_categories.return_value': dict(),
            'return_value.get_alternatives.return_value': list(),
        }

    @patch('products.views.CheckProduct')
    def test_search_product_good_template(self, MockCheckProduct):
        MockCheckProduct.configure_mock(**self.attrs)
        self.client.get(f'/products/product/{self.code}/')

        self.assertTemplateUsed('products/product.html')

    @patch('products.views.CheckProduct')
    def test_search_product_good_context(self, MockCheckProduct):
        MockCheckProduct.configure_mock(**self.attrs)
        response = self.client.get(f'/products/product/{self.code}/')
        self.assertIn(
            'product',
            response.context
        )
        self.assertNotIn(
            'user_products',
            response.context
        )
        self.assertIsInstance(
            response.context['product'],
            object
        )

    @patch('products.views.CheckProduct')
    def test_search_product_good_context_user_connected(self, MockCheckProduct):
        MockCheckProduct.configure_mock(**self.attrs)
        self.client.login(**self.user)
        response = self.client.get(f'/products/product/{self.code}/')
        self.assertIn(
            'product',
            response.context
        )
        self.assertIn(
            'user_products',
            response.context
        )
        self.assertIsInstance(
            response.context['product'],
            object
        )


class UserProductsTest(TestCase):
    """Testing user product view"""

    fixtures = ['users.json']

    def setUp(self):
        self.user = {
            'username': 'foo@example.com',
            'password': 'admin'
        }
        self.attrs = {
            'return_value.get_user_products.return_value': list(),
        }

    def test_search_user_products_user_not_connected(self):
        response = self.client.get(f'/products/my_products/')

        self.assertNotEqual(response.status_code, 200)

    @patch('products.views.UserProducts')
    def test_search_user_products_user_connected(self, MockUserProducts):
        MockUserProducts.configure_mock(**self.attrs)

        self.client.login(**self.user)
        response = self.client.get(f'/products/my_products/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('products/my_products.html')

    @patch('products.views.UserProducts')
    def test_search_user_products_check_context(self, MockUserProducts):
        MockUserProducts.configure_mock(**self.attrs)

        self.client.login(**self.user)
        response = self.client.get(f'/products/my_products/')

        self.assertIn(
            'products',
            response.context
        )
        self.assertIsInstance(
            response.context['products'],
            list
        )

class SaveViewTest(TestCase):
    """Test save view"""

    fixtures = ['users.json']

    def setUp(self):
        self.user = {
            'username': 'foo@example.com',
            'password': 'admin'
        }
        self.form = {'products_to_save': 'some_products'}

    @patch('products.views.SaveView.form_class')
    def test_save_products_user_not_connected(self, MockSaveForm):
        MockSaveForm.return_value.is_valid.return_value = True
        response = self.client.post(
            '/products/save',
            self.form
        )
        self.assertNotEqual(response.status_code, 200)

    @patch('products.views.SaveView.form_class')
    def test_save_products_user_connected(self, MockSaveForm):
        MockSaveForm.return_value.is_valid.return_value = True
        MockSaveForm.return_value.save_products.return_value = True
        self.client.login(**self.user)
        response = self.client.post(
            '/products/save',
            self.form
        )
        self.assertRedirects(
            response,
            '/products/my_products/',
            fetch_redirect_response=False
        )


class DeleteViewTest(TestCase):
    """Test delete view"""

    fixtures = ['users.json']

    def setUp(self):
        self.user = {
            'username': 'foo@example.com',
            'password': 'admin'
        }
        self.form = {'products_to_delete': 'some_products'}

    @patch('products.views.DeleteView.form_class')
    def test_delete_products_user_not_connected(self, MockDeleteForm):
        MockDeleteForm.return_value.is_valid.return_value = True
        response = self.client.post(
            '/products/delete',
            self.form
        )
        self.assertNotEqual(response.status_code, 200)

    @patch('products.views.DeleteView.form_class')
    def test_delete_products_user_connected(self, MockDeleteForm):
        MockDeleteForm.return_value.is_valid.return_value = True
        MockDeleteForm.return_value.save_products.return_value = True
        self.client.login(**self.user)
        response = self.client.post(
            '/products/delete',
            self.form
        )
        self.assertRedirects(
            response,
            '/products/my_products/',
            fetch_redirect_response=False
        )

