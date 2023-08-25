#!/usr/bin/env python
"""Tests for Django web urls"""

## Django
from django.test import TestCase, Client
from django.urls import reverse

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
        self.client = Client()
    
    def test_dasboard_url_is_accessible(self):
        """
        Test case for checking availability of the / URL
        """
        response = self.client.get(reverse('web-dashboard'))
        self.assertEqual(response.status_code, 200)
        dashboard_title = "<title>spot-utils - Dashboard</title>"
        self.assertTrue(dashboard_title in response.content.decode('utf-8'))
    
    def test_auth_url_is_accessible(self):
        """
        Test case for checking availability of the /auth/ URL
        """
        response = self.client.get(reverse('web-auth'))
        self.assertEqual(response.status_code, 200)
        auth_title = "<title>spot-utils - Auth</title>"
        self.assertTrue(auth_title in response.content.decode('utf-8'))
    
    def test_pointcloud_url_is_accessible(self):
        """
        Test case for checking availability of the /pointcloud/ URL
        """
        name = 'fake_pointcloud_name'
        response = self.client.get(reverse('web-pointcloud', args=[name]))
        self.assertEqual(response.status_code, 200)
        pointcloud_title = "<title>spot-utils - Potree Viewer</title>"
        self.assertTrue(pointcloud_title in response.content.decode('utf-8'))
    
    def test_pointcloud_index_url_is_accessible(self):
        """
        Test case for checking availability of the /pointcloud_index/ URL
        """
        response = self.client.get(reverse('web-pointcloud-index'))
        self.assertEqual(response.status_code, 200)
        pointcloud_title = "<title>spot-utils - Pointcloud Index</title>"
        self.assertTrue(pointcloud_title in response.content.decode('utf-8'))
