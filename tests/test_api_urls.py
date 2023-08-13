#!/usr/bin/env python
"""Tests for Django api urls"""

# Imports
import mock
import json

## Django
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.response import Response

def mocked_helloSpot_get(*args):
    return Response('Hello, Spot!')

def mocked_get_camera_feed(*args):
    return Response('camera')

def mocked_close_camera_feed(*args):
    return Response('closed camera')

def mocked_open_ricoh_camera_feed(*args):
    return Response('started SpotCameras')

def mocked_stop_ricoh_camera_feed(*args):
    return Response('stopped SpotCameras')

def mocked_get_pointclouds(*args):
    return Response('pointcloud list')

def mocked_collect_pointclouds(*args):
    return Response('collected pointclouds')

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

    def test_api_routes_route_is_accessible(self):
        """
        Test case for checking availability of the GET /api/ API route
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

    @mock.patch('api.views.HelloSpot.get', mocked_helloSpot_get)
    def test_hellospot_route_is_accessible(self):
        """
        Test case for checking availability of the GET /api/hello-spot/ API route
        """
        response = self.client.get(reverse('api-hello-spot'))
        self.assertEqual(response.status_code, 200)

    @mock.patch('api.views.SpotCameras.get', mocked_get_camera_feed)
    def test_camera_route_is_accessible(self):
        """
        Test case for checking availability of the GET /api/camera/ API route
        """
        response = self.client.get(reverse('api-camera'))
        self.assertEqual(response.status_code, 200)
    
    @mock.patch('api.views.SpotCameras.delete', mocked_close_camera_feed)
    def test_close_camera_route_is_accessible(self):
        """
        Test case for checking availability of the DELETE /api/camera/ API route
        """
        response = self.client.delete(reverse('api-camera'))
        self.assertEqual(response.status_code, 200)
    
    @mock.patch('api.views.SpotCamerasImageService.get', mocked_open_ricoh_camera_feed)
    def test_spot_cameras_route_is_accessible(self):
        """
        Test case for checking availability of the GET /api/spot-cameras/ API route
        """
        response = self.client.get(reverse('api-spot-cameras'))
        self.assertEqual(response.status_code, 200)
    
    @mock.patch('api.views.SpotCamerasImageService.delete', mocked_stop_ricoh_camera_feed)
    def test_stop_spot_cameras_route_is_accessible(self):
        """
        Test case for checking availability of the DELETE /api/spot-cameras/ API route
        """
        response = self.client.delete(reverse('api-spot-cameras'))
        self.assertEqual(response.status_code, 200)
    
    @mock.patch('api.views.Pointclouds.get', mocked_get_pointclouds)
    def test_get_pointclouds_route_is_accessible(self):
        """
        Test case for checking availability of the GET /api/pointclouds/ API route
        """
        response = self.client.get(reverse('api-pointclouds'))
        self.assertEqual(response.status_code, 200)
    
    @mock.patch('api.views.Pointclouds.post', mocked_collect_pointclouds)
    def test_collect_pointclouds_route_is_accessible(self):
        """
        Test case for checking availability of the POST /api/pointclouds/ API route
        """
        response = self.client.post(reverse('api-pointclouds'))
        self.assertEqual(response.status_code, 200)
