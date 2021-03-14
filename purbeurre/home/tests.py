"""Module home.tests"""
from django.apps import apps
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from unittest.mock import patch

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

class HomeViewTests(TestCase):
    """Testing home view"""

    def test_home_view(self):
        """Test get user home"""

        self.client.get('/')

        self.assertTemplateUsed('home.html')

    def test_legals(self):
        """Test legals page"""

        self.client.get('/legal_notice/')

        self.assertTemplateUsed('legal_notice.html')
