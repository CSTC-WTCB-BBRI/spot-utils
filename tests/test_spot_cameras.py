#!/usr/bin/env python
"""Tests for the python script spotCameras.py"""

# Imports
import mock

## Django
from django.test import TestCase

# Local Imports
from api.scripts.spotCameras import WebCam

# Main
class WebCamTestCase(TestCase):
    """
    Test cases for the WebCam Camera Interface.
    """
    device_name = ''

    def setUp(self):
        """
        This method is ran before each test case in this class.
        """
        pass
    
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
