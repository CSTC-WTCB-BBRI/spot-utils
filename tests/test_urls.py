#!/usr/bin/env python
"""Tests for Django urls"""

# Imports
import mock

## Django
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.response import Response

# Local imports
import api.scripts.helloSpot

# Main
class WebUrlsTestCase(TestCase):
    """
    Test cases for the Django web app urls.
    """
    client = None

    def setUp(self):
        """
        This method is ran before each test case in this class.
            Initialisation of a new Client instance.
        """
        client = Client()
    
    def test_dasboard_url_is_accessible(self):
        """
        Test case for checking availability of the / URL
        """
        response = self.client.get(reverse('web-dashboard'))
        self.assertEqual(response.status_code, 200)
        dashboard_title = "<title>spot-utils - dashboard</title>"
        self.assertTrue(dashboard_title in response.content.decode('utf-8'))
    
    def test_auth_url_is_accessible(self):
        """
        Test case for checking availability of the /auth/ URL
        """
        response = self.client.get(reverse('web-auth'))
        self.assertEqual(response.status_code, 200)
        auth_title = "<title>spot-utils - auth</title>"
        self.assertTrue(auth_title in response.content.decode('utf-8'))
    
    def test_pointcloud_url_is_accessible(self):
        """
        Test case for checking availability of the /pointcloud/ URL
        """
        response = self.client.get(reverse('web-pointcloud'))
        self.assertEqual(response.status_code, 200)
        pointcloud_title = "<title>spot-utils - pointcloud</title>"
        self.assertTrue(pointcloud_title in response.content.decode('utf-8'))

class ApiUrlsTestCase(TestCase):
    """
    Test cases for the Django api app urls.
    """
    client = None

    def setUp(self):
        """
        This method is ran before each test case in this class.
            Initialisation of a new Client instance.
        """
        client = Client()

    def mocked_helloSpot_get(*args):
        return Response('Hello, Spot!')
    
    def test_apiroutes_route_is_accessible(self):
        """
        Test case for checking availability of the /api/ API route
        and that the response contains data
        """
        response = self.client.get(reverse('api-routes'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)
    
    @mock.patch('api.views.HelloSpot.get', mocked_helloSpot_get)
    def test_hellospot_route_is_accessible(self):
        """
        Test case for checking availability of the /api/hello-spot/ API route
        """
        response = self.client.get(reverse('api-hello-spot'))
        self.assertEqual(response.status_code, 200)