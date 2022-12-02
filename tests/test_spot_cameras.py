#!/usr/bin/env python
"""Tests for the spot_cameras Python script"""

# Imports
import mock
import cv2 as cv
import numpy as np

## Bosdyn
from bosdyn.client.image import ImageClient
from bosdyn.api.image_pb2 import ImageResponse

## Django
from django.test import TestCase

# Local imports
from api.scripts.spot_cameras import SpotCameras

# Main
class SpotCamerasTestCase(TestCase):
    """
    Test cases for the spot_cameras Python script.
    """
    spotCameras = None
    cameras = {
        'back_fisheye_image': 'back_fisheye_image',
        'frontleft_fisheye_image': 'frontleft_fisheye_image',
        'frontright_fisheye_image': 'frontright_fisheye_image',
        'left_fisheye_image': 'left_fisheye_image',
        'right_fisheye_image': 'right_fisheye_image'
    }

    def mocked_get_image(self):
        pass
    
    def mocked_get_image_from_sources(self, image_sources, **kwargs):
        img = ImageResponse()
        img.source.name = 'left_fisheye_image'
        return [img]
    
    @mock.patch('bosdyn.client.image.ImageClient.get_image_from_sources', mocked_get_image_from_sources)
    @mock.patch('api.scripts.spot_cameras.SpotCameras.getImage', mocked_get_image)
    def setUp(self):
        """
        This method is ran before each test case in this class.
            Initialisation of a new SpotCameras instance.
        """
        camera_index = '0'
        image_client = ImageClient()
        self.spotCameras = SpotCameras(camera_index, image_client)
    
    def test_spot_cameras_constructor(self):
        """
        Test Case for checking the SpotCameras constructor.
        """
        self.assertEqual(self.spotCameras.cameras, self.cameras)
        self.assertEqual(self.spotCameras.frame, None)
        self.assertTrue(isinstance(self.spotCameras.image_client, ImageClient))

    def mocked_imdecode(buf, flags):
        img = cv.imread("./tests/test.jpg")
        return img
    
    def mocked_rotate(img, angle):
        return img

    @mock.patch('scipy.ndimage.rotate', mocked_rotate)
    @mock.patch('cv2.imdecode', mocked_imdecode)
    @mock.patch('bosdyn.client.image.ImageClient.get_image_from_sources', mocked_get_image_from_sources)
    def test_get_image(self):
        """
        Test Case for checking the getImage method.
        """
        self.spotCameras.getImage()
