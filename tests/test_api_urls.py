#!/usr/bin/env python
"""Tests for Django api urls"""

# Imports
import json

## Django
from django.test import TestCase, Client
from django.urls import reverse, resolve

# Local Imports
from api.views import *

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
        self.client = Client()

    def test_api_routes_endpoint_is_accessible(self):
        """
        Test case for checking availability of the GET /api/ API routte
        """
        response = self.client.get(reverse('api-routes'))
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        self.assertIsInstance(content, list)

        for route in content:
            # Check that each route object has the expected fields
            self.assertIn('endpoint', route)
            self.assertIn('method', route)
            self.assertIn('body', route)
            self.assertIn('description', route)
            
            # Check the data types of the fields
            self.assertIsInstance(route['endpoint'], str)
            self.assertIsInstance(route['method'], str)
            self.assertIsInstance(route['description'], str)
            
            # Check that the method field contains a valid HTTP verb
            valid_http_verbs = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
            self.assertIn(route['method'], valid_http_verbs)

    def test_hellospot_endpoint_is_accessible(self):
        """
        Test case for checking availability of the /api/hello-spot/ API endpoints (only GET)
        """
        url = reverse('api-hello-spot')
        match = resolve(url)
        self.assertEqual(match.func.__module__, HelloSpot.__module__)

        view_class = match.func.view_class
        self.assertTrue(hasattr(view_class, 'get'))
        self.assertFalse(hasattr(view_class, 'post'))

    def test_camera_route_is_accessible(self):
        """
        Test case for checking availability of the GET /api/camera/ API route
        """
        url = reverse('api-get-camera-feed')
        match = resolve(url)
        self.assertEqual(match.func, getCameraFeed)
    
    def test_close_camera_route_is_accessible(self):
        """
        Test case for checking availability of the DELETE /api/close-camera/ API route
        """
        url = reverse('api-close-camera')
        match = resolve(url)
        self.assertEqual(match.func, closeCameraFeed)
    
    
    def test_spot_cameras_route_is_accessible(self):
        """
        Test case for checking availability of the GET /api/start-spot-cameras/ API route
        """
        url = reverse('api-start-spot-cameras')
        match = resolve(url)
        self.assertEqual(match.func, startSpotCamerasImageServiceView)
    
    def test_stop_spot_cameras_route_is_accessible(self):
        """
        Test case for checking availability of the DELETE /api/stop-spot-cameras/ API route
        """
        url = reverse('api-stop-spot-cameras')
        match = resolve(url)
        self.assertEqual(match.func, stopSpotCamerasImageServiceView)
    
    def test_pointclouds_endpoints_are_accessible(self):
        """
        Test case for checking availability of the /api/pointclouds/ API endpoints (GET & POST)
        """
        url = reverse('api-pointclouds')
        match = resolve(url)
        self.assertEqual(match.func.__module__, Pointclouds.__module__)

        view_class = match.func.view_class
        self.assertTrue(hasattr(view_class, 'get'))
        self.assertTrue(hasattr(view_class, 'post'))
    
    def test_spot_slam_endpoints_are_accessible(self):
        """
        Test case for checking availability of the /api/spot-slam/ API endpoints (POST with multiple url params)
        """
        url = reverse('api-spot-slam')
        match = resolve(url)
        self.assertEqual(match.func.__module__, SpotSLAM.__module__)

        view_class = match.func.view_class
        self.assertFalse(hasattr(view_class, 'get'))
        self.assertTrue(hasattr(view_class, 'post'))
