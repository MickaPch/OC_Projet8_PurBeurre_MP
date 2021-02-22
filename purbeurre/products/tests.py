from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.test import TestCase, RequestFactory, Client

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
from user.models import User


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

    def test_app_(self):
        """Test app name"""
        self.assertEqual(
            ProductsConfig.name,
            'products'
        )
        self.assertEqual(
            apps.get_app_config('products').name,
            'products'
        )

class ProductsViewTest(TestCase):
    """Testing products view"""
    def setUp(self):
        initiate_test_db()

    def test_products_view(self):
        """Test products post / all search types"""
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
            response = self.client.get(
                '/search/',
                search_form,
                follow=True
            )
            self.assertEqual(response.status_code, 200)

    def test_products_form_invalid_view(self):
        """Test products post / invalid_form"""
        search_form = {
            'product_search': 'test',
            'type': 'wrong_type'
        }
        response = self.client.get(
            '/search/',
            search_form,
            follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_products_by_code_view(self):
        """Test products post / product_code"""

        search_form = {
            'product_search': '123456789',
            'type': 'search'
        }
        client = Client(
            HTTP_HOST='localhost'
        )
        # request = RequestFactory()

        response = client.get(
            '/search/',
            search_form
        )
        self.assertEqual(response.status_code, 302)

class ProductViewTest(TestCase):
    """Testing product view"""

    def setUp(self):
        initiate_test_db()
        self.product_form = {
            'product_code': '123456789'
        }
        self.client.login(
            username='foo@example.com',
            password='admin'
        )


    def test_get_product(self):
        """Test get a product"""
        
        response = self.client.get(
            '/product/',
            self.product_form,
            follow=True
        )
        self.assertEqual(response.status_code, 200)

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
