# Copyright (c) 2022 Boston Dynamics, Inc.  All rights reserved.
#
# Downloading, reproducing, distributing or otherwise using the SDK Software
# is subject to the terms and conditions of the Boston Dynamics Software
# Development Kit License (20191101-BDSDK-SL).

# See https://github.com/boston-dynamics/spot-sdk/blob/master/python/examples/web_cam_image_service/web_cam_image_service.py for the original file

#!/usr/bin/env python
"""Services for fetching live video feed from spot's cameras"""

# Imports
import logging
import cv2
import time

# Boston Dynamics
from bosdyn.client.image_service_helpers import CameraInterface, convert_RGB_to_grayscale, VisualImageSource, CameraBaseImageServicer
from bosdyn.api import image_pb2

# Local Imports

# Variables
_LOGGER = logging.getLogger(__name__)

# Main
class WebCam(CameraInterface):
    """Provide access to the latest webcam data using openCV's VideoCapture."""
    def __init__(self, device_name, default_jpeg_quality=75):
        """
        Construct a new WebCam instance

            Parameters:
                device_name (str): camera device name (integer-convertible)
                default_jpeg_quality (int): default jpeg image quality
        """
        self.device_name = int(device_name)
        self.image_source_name = "video" + str(device_name)
        self.capture = cv2.VideoCapture(self.device_name)
        if not self.capture.isOpened():
            err = "Unable to open a cv2.VideoCapture connection to %s" % self.device_name
            _LOGGER.warning(err)
            raise Exception(err)

        self.camera_exposure, self.camera_gain = None, None
        try:
            self.camera_gain = self.capture.get(cv2.CAP_PROP_GAIN)
        except cv2.error as e:
            _LOGGER.warning("Unable to determine camera gain: %s", e)
        try:
            self.camera_exposure = self.capture.get(cv2.CAP_PROP_EXPOSURE)
        except cv2.error as e:
            _LOGGER.warning("Unable to determine camera exposure time: %s", e)
        self.rows = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.cols = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))

        self.default_jpeg_quality = default_jpeg_quality
    
    def blocking_capture(self):
        capture_time = time.time()
        success, image = self.capture.read()
        if success:
            return image, capture_time
        else:
            raise Exception("Unsuccessful call to cv2.VideoCapture().read()")
    
    def image_decode(self, image_data, image_proto, image_req):
        pixel_format = image_req.pixel_format
        converted_image_data = image_data
        if pixel_format == image_pb2.Image.PIXEL_FORMAT_GREYSCALE_U8:
            converted_image_data = convert_RGB_to_grayscale(
                cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB))

        if pixel_format == image_pb2.Image.PIXEL_FORMAT_UNKNOWN:
            image_proto.pixel_format = image_pb2.Image.PIXEL_FORMAT_RGB_U8
        else:
            image_proto.pixel_format = pixel_format
        
        resize_ratio = image_req.resize_ratio
        quality_percent = image_req.quality_percent
        if resize_ratio < 0 or resize_ratio > 1:
            raise ValueError("Resize ratio %s is out of bounds." % resize_ratio)

        if resize_ratio != 1.0 and resize_ratio != 0:
            image_proto.rows = int(image_proto.rows * resize_ratio)
            image_proto.cols = int(image_proto.cols * resize_ratio)
            converted_image_data = cv2.resize(converted_image_data, (image_proto.cols, image_proto.rows), interpolation = cv2.INTER_AREA)

        # Set the image data.
        image_format = image_req.image_format
        if image_format == image_pb2.Image.FORMAT_RAW:
            image_proto.data = np.ndarray.tobytes(converted_image_data)
            image_proto.format = image_pb2.Image.FORMAT_RAW
        
        elif image_format == image_pb2.Image.FORMAT_JPEG or image_format == image_pb2.Image.FORMAT_UNKNOWN or image_format is None:
            quality = self.default_jpeg_quality
            if 0 < quality_percent <= 100:
                quality = quality_percent
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), int(quality)]
            image_proto.data = cv2.imencode('.jpg', converted_image_data, encode_param)[1].tobytes()
            image_proto.format = image_pb2.Image.FORMAT_JPEG
        
        else:
            raise Exception(
                "Image format %s is unsupported." % image_pb2.Image.Format.Name(image_format))
        
    def make_webcam_image_service(bosdyn_sdk_robot, service_name, device_names, logger=None):
        image_sources = []
        for device in device_names:
            web_cam = WebCam(device)
            img_src = VisualImageSource(web_cam.image_source_name, web_cam, rows=web_cam.rows,
                                        cols=web_cam.cols, gain=web_cam.camera_gain,
                                        exposure=web_cam.camera_exposure,
                                        pixel_formats=[image_pb2.Image.PIXEL_FORMAT_GREYSCALE_U8,
                                                    image_pb2.Image.PIXEL_FORMAT_RGB_U8])
            image_sources.append(img_src)
            return CameraBaseImageServicer(bosdyn_sdk_robot, service_name, image_sources, logger)
