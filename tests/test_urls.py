#!/usr/bin/env python
"""Tests for Django urls"""

# Imports
import mock

## Django
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.response import Response
from django.http import HttpResponse

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

    def mocked_get_camera_feed(*args):
        return HttpResponse('cameras')
    
    @mock.patch('api.views.getCameraFeed', mocked_get_camera_feed)
    def test_camera_route_is_accessible(self):
        """
        Test case for checking availability of the /api/camera/ API route
        """
        response = self.client.get(reverse('api-get-camera-feed'))
        self.assertEqual(response.status_code, 200)

    def mocked_close_camera_feed(*args):
        return HttpResponse('closed camera')
    
    @mock.patch('api.views.closeCameraFeed', mocked_close_camera_feed)
    def test_close_camera_route_is_accessible(self):
        """
        Test case for checking availability of the /api/camera/ API route
        """
        response = self.client.get(reverse('api-close-camera'))
        self.assertEqual(response.status_code, 200)

    def mocked_stop_gst_loopback(*args):
        return HttpResponse('stopped gst_loopback')
    
    @mock.patch('api.views.stopGstLoopbackView', mocked_stop_gst_loopback)
    def test_stop_gst_loopback_route_is_accessible(self):
        """
        Test case for checking availability of the /api/stop-gst-loopback/ API route
        """
        response = self.client.get(reverse('api-stop-gst-loopback'))
        self.assertEqual(response.status_code, 200)

    def mocked_start_spot_cameras_image_service(*args):
        return HttpResponse('started SpotCameras')
    
    @mock.patch('api.views.startSpotCamerasImageServiceView', mocked_start_spot_cameras_image_service)
    def test_start_gst_loopback_route_is_accessible(self):
        """
        Test case for checking availability of the /api/start-spot-cameras/ API route
        """
        response = self.client.get(reverse('api-start-spot-cameras'))
        self.assertEqual(response.status_code, 200)
