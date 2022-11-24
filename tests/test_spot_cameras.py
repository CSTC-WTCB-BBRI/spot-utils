#!/usr/bin/env python
"""Tests for the python script spotCameras.py"""

# Imports
import mock
import cv2
import imghdr
from io import BytesIO
from PIL import Image

## Django
from django.test import TestCase

## Boston Dynamics
import bosdyn.client.util
from bosdyn.api import image_pb2
from bosdyn.client.image import build_image_request

# Local Imports
from api.scripts.spotCameras import WebCam, make_webcam_image_service

# Main
class WebCamTestCase(TestCase):
    """
    Test cases for the WebCam Camera Interface.
    """
    # Constants
    MOCKED_CAMERA_GAIN = 10
    MOCKED_CAMERA_EXPOSURE = 150
    MOCKED_CAMERA_ROWS = 200
    MOCKED_CAMERA_COLS = 100
    SERVICE_NAME = 'SpotCameras'
    CLIENT_NAME = 'Test Spot'
    ROBOT_IP="0.0.0.0"
    WEBCAM_PORT=5000

    def setUp(self):
        """
        This method is ran before each test case in this class.
        """
        self.device_name = '0'
    
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
        if propId == cv2.CAP_PROP_GAIN:
            return WebCamTestCase.MOCKED_CAMERA_GAIN
        elif propId == cv2.CAP_PROP_EXPOSURE:
            return WebCamTestCase.MOCKED_CAMERA_EXPOSURE
        elif propId == cv2.CAP_PROP_FRAME_HEIGHT:
            return WebCamTestCase.MOCKED_CAMERA_ROWS
        elif propId == cv2.CAP_PROP_FRAME_WIDTH:
            return WebCamTestCase.MOCKED_CAMERA_COLS
        else:
            return 0

    @mock.patch('cv2.VideoCapture.get', mocked_capture_get)
    def test_get_capture_constants_from_known_device(self):
        """
        Test case for checking the device camera gain and exposure are saved in instance variables.
            Also test that the image dimensions are saved in instance variables.
        """
        webCam = WebCam(self.device_name)
        self.assertEqual(webCam.camera_gain, self.MOCKED_CAMERA_GAIN)
        self.assertEqual(webCam.camera_exposure, self.MOCKED_CAMERA_EXPOSURE)
        self.assertEqual(webCam.rows, self.MOCKED_CAMERA_ROWS)
        self.assertEqual(webCam.cols, self.MOCKED_CAMERA_COLS)
    
    def mocked_capture_read_unsuccesful(self):
        image = Image.open("tests/src/test.jpeg")
        return False, image
    
    def mocked_capture_read_succesful(self):
        image = Image.open("tests/src/test.jpeg")
        return True, image

    @mock.patch('cv2.VideoCapture.read', mocked_capture_read_unsuccesful)
    def test_blocking_capture_raises_exception_when_unsuccesful(self):
        """
        Test case for checking that an unsuccesful capture raises an exception.
        """
        webCam = WebCam(self.device_name)
        self.assertRaises(Exception, webCam.blocking_capture)

    @mock.patch('cv2.VideoCapture.read', mocked_capture_read_succesful)
    def test_blocking_capture_returns_jpeg_image(self):
        """
        Test case for checking that a succesful capture returns a jpeg image.
        """
        webCam = WebCam(self.device_name)
        image, capture_time = webCam.blocking_capture()
        self.assertEqual(image.format, 'JPEG')
    
    # def test_decoded_image_format(self):
    #     """
    #     Test case for checking that the decoded image's format.
    #     """
    #     webCam = WebCam(self.device_name)
    #     image, capture_time = webCam.blocking_capture()
    #     image_proto = image_pb2.Image()
    #     image_req = build_image_request('test', webCam.default_jpeg_quality, image_pb2.Image.FORMAT_JPEG, image_pb2.Image.PIXEL_FORMAT_GREYSCALE_U8, None)
    #     webCam.image_decode(image, image_proto, image_req)

    def mocked_camera_base_image_servicer_constructor(self, bosdyn_sdk_robot, service_name, image_sources, logger):
        self.image_sources_mapped = dict()
        self.service_name = service_name
        self.image_sources = image_sources

    @mock.patch('cv2.VideoCapture.get', mocked_capture_get)
    @mock.patch('bosdyn.client.image_service_helpers.CameraBaseImageServicer.__init__', mocked_camera_base_image_servicer_constructor)
    def test_service_servicer_creation(self):
        """
        Test case for checking the service servicer creation.
        """
        device_names = [self.device_name]
        sdk = bosdyn.client.create_standard_sdk(self.CLIENT_NAME)
        robot = sdk.create_robot(self.ROBOT_IP)
        service_servicer = make_webcam_image_service(robot, self.SERVICE_NAME, device_names)
        deviceIdxO_params = service_servicer.image_sources[0].get_image_capture_params()
        self.assertEqual(service_servicer.service_name, self.SERVICE_NAME)
        self.assertEqual(service_servicer.image_sources[0].image_source_proto.rows, self.MOCKED_CAMERA_ROWS)
        self.assertEqual(service_servicer.image_sources[0].image_source_proto.cols, self.MOCKED_CAMERA_COLS)
        self.assertEqual(deviceIdxO_params.gain, self.MOCKED_CAMERA_GAIN)
        self.assertEqual(deviceIdxO_params.exposure_duration.seconds, self.MOCKED_CAMERA_EXPOSURE)

    # @mock.patch('bosdyn.client.image_service_helpers.CameraBaseImageServicer.__init__', mocked_camera_base_image_servicer_constructor)
    # def mocked_make_webcam_image_service(self, bosdyn_sdk_robot, service_name, device_names, logger=None):
    #     return CameraBaseImageServicer(bosdyn_sdk_robot, service_name, image_sources, logger)
    
    # @mock.patch('api.scripts.spotCameras.WebCam.make_webcam_image_service', mocked_make_webcam_image_service)
    # def test_run_service(self):
    #     """
    #     Test case for running the image service.
    #     """
    #     device_names = [self.device_name]
    #     sdk = bosdyn.client.create_standard_sdk(self.CLIENT_NAME)
    #     robot = sdk.create_robot(self.ROBOT_IP)
    #     WebCam.run_service(robot, self.WEBCAM_PORT, self.SERVICE_NAME, device_names)
