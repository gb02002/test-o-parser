import logging

from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch, Mock

from parsing_app.models import Products
from parsing_app.views import Parser_Init


class YourViewTestCase(TestCase):
    @patch('parsing_app.views.Parser_Init.get_product_data')
    def test_get_success(self, mock_get_product_data):
        mock_get_product_data.return_value = {"id": 1, "name": "Test Product"}

        response = self.client.get(reverse('view-products'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"id": 1, "name": "Test Product"})

    @patch('parsing_app.views.Parser_Init.get_product_data')
    def test_get_no_content(self, mock_get_product_data):
        mock_get_product_data.return_value = None

        response = self.client.get(reverse('view-products'))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"No content"})



