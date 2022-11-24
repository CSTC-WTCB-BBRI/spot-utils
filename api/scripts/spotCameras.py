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

# Boston Dynamics
from bosdyn.client.image_service_helpers import CameraInterface

# Local Imports

# Variables
_LOGGER = logging.getLogger(__name__)

# Main
class WebCam(CameraInterface):
    """Provide access to the latest web cam data using openCV's VideoCapture."""
    def __init__(self, device_name):
        """
        Construct a new WebCam instance

            Parameters:
                device_name (str): camera device name (integer-convertible)
        """
        self.device_name = int(device_name)
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
    
    def blocking_capture(self):
        pass
    
    def image_decode(self, image_data, image_proto, image_req):
        pass
