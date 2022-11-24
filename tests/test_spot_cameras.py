#!/usr/bin/env python
"""Tests for the python script spotCameras.py"""

# Imports
import mock
import cv2

## Django
from django.test import TestCase

# Local Imports
from api.scripts.spotCameras import WebCam

# Main
class WebCamTestCase(TestCase):
    """
    Test cases for the WebCam Camera Interface.
    """
    # Constants
    mocked_camera_gain = 10
    mocked_camera_exposure = 150
    mocked_camera_rows = 200
    mocked_camera_cols = 100

    def setUp(self):
        """
        This method is ran before each test case in this class.
        """
        self.device_name = ''
    
    def test_device_name_not_integer_raises_value_error_exception(self):
        """
        Test case for checking that a non integer-convertible device_name (string) passed to the
            WebCam class constructor raises an exception
        """
        self.device_name = 'not an int'
        self.assertRaises(ValueError, WebCam, self.device_name)
    
    def test_unknown_device_name_raises_exception(self):
        """
        Test case for checking an unknown device name raises an exception.
        """
        self.device_name = '666'
        self.assertRaises(Exception, WebCam, self.device_name)
    
    def mocked_capture_get(self, propId):
        match propId:
            case cv2.CAP_PROP_GAIN:
                return WebCamTestCase.mocked_camera_gain
            case cv2.CAP_PROP_EXPOSURE:
                return WebCamTestCase.mocked_camera_exposure
            case cv2.CAP_PROP_FRAME_HEIGHT:
                return WebCamTestCase.mocked_camera_rows
            case cv2.CAP_PROP_FRAME_WIDTH:
                return WebCamTestCase.mocked_camera_cols
            case other:
                return 0

    @mock.patch('cv2.VideoCapture.get', mocked_capture_get)
    def test_get_capture_constants_from_known_device(self):
        """
        Test case for checking the device camera gain and exposure are saved in instance variables.
            Also test that the image dimensions are saved in instance variables.
        """
        self.device_name = '0'
        webCam = WebCam(self.device_name)
        self.assertEqual(webCam.camera_gain, self.mocked_camera_gain)
        self.assertEqual(webCam.camera_exposure, self.mocked_camera_exposure)
        self.assertEqual(webCam.rows, self.mocked_camera_rows)
        self.assertEqual(webCam.cols, self.mocked_camera_cols)
