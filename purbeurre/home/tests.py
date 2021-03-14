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

    @patch('home.views.SearchForm')
    @patch('home.views.ConnectionForm')
    def test_home_view(self, MockConnectionForm, MockSearchForm):
        """Test get user home"""
        MockConnectionForm.assert_not_called()
        MockSearchForm.assert_not_called()

        self.client.get(
            '/'
        )

        self.assertTemplateUsed('home.html')

        MockConnectionForm.assert_called_once()
        MockSearchForm.assert_called_once()

    @patch('home.views.SearchForm')
    @patch('home.views.ConnectionForm')
    def test_legals(self, MockConnectionForm, MockSearchForm):
        """Test legals page"""

        MockConnectionForm.assert_not_called()
        MockSearchForm.assert_not_called()

        self.client.get('/legal_notice/')

        self.assertTemplateUsed('legal_notice.html')

        MockConnectionForm.assert_called_once()
        MockSearchForm.assert_called_once()
