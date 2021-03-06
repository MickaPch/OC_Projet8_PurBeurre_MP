"""Module home.tests"""
from django.apps import apps
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser

from home.apps import HomeConfig


class HomeConfigTest(TestCase):
    """Testing home app"""

    def test_app_(self):
        """Test app name"""
        self.assertEqual(
            HomeConfig.name,
            'home'
        )
        self.assertEqual(
            apps.get_app_config('home').name,
            'home'
        )

class HomeViewTest(TestCase):
    """Testing home view"""

    def setUp(self):
        self.factory = RequestFactory()

    def test_home_view(self):
        """Test get user home"""

        response = self.client.get(
            '/'
        )

        self.assertEqual(response.status_code, 200)
