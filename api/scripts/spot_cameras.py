#!/usr/bin/env python
"""Allows querrying Spot's Image Services"""

# Imports
import numpy as np
from scipy import ndimage
import cv2 as cv
import threading
import time

## Boston Dynamics
import bosdyn.client
from bosdyn.api import image_pb2

# Variables
ROTATION_ANGLE = {
    'back_fisheye_image': 0,
    'frontleft_fisheye_image': -90,
    'frontright_fisheye_image': -90,
    'left_fisheye_image': 0,
    'right_fisheye_image': 180,
    'video99': 0
}

# Main
class SpotCameras(object):
    """
    Provides an interface of communication with Spot's Image Services.
    """
    def __init__(self, camera_request, image_client):
        """
        Construct a new SpotCameras instance

            Parameters:
                camera_request (str): Camera requested
                image_client (Client): Client for Spot's Image Service
        """
        self.frame = None
        self.camera_request = camera_request
        self.image_client = image_client
        self.getImage()
        self.updating = True
        threading.Thread(target=self.update, args=()).start()
    
    def __del__(self):
        """
        Stops the interface from updating the frame.
        """
        self.updating = False
    
    def getImage(self):
        """
        Querries Spot's Image Service to get a capture of the required camera.
        """
        image_responses = self.image_client.get_image_from_sources([self.camera_request])
        image = image_responses[0]
        num_bytes = 1
        if image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_DEPTH_U16:
            dtype = np.uint16
            extension = ".png"
        else:
            if image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_RGB_U8:
                num_bytes = 3
            elif image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_RGBA_U8:
                num_bytes = 4
            elif image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_GREYSCALE_U8:
                num_bytes = 1
            elif image.shot.image.pixel_format == image_pb2.Image.PIXEL_FORMAT_GREYSCALE_U16:
                num_bytes = 2
            dtype = np.uint8
            extension = ".jpg"
        img = np.frombuffer(image.shot.image.data, dtype=dtype)
        if image.shot.image.format == image_pb2.Image.FORMAT_RAW:
            try:
                img = img.reshape((image.shot.image.rows, image.shot.image.cols, num_bytes))
            except ValueError:
                img = cv.imdecode(img, -1)
        else:
            img = cv.imdecode(img, -1)
        img = ndimage.rotate(img, ROTATION_ANGLE[image.source.name])
        self.frame = img

    def get_frame(self):
        """
        Encodes the frame in JPG.
        """
        frame = self.frame
        try:
            _, jpeg = cv.imencode('.jpg', frame)
            return jpeg.tobytes()
        except:
            return False
    
    def update(self):
        """
        Updates the stored frame.
        """
        while self.updating:
            self.getImage()

def gen(camera):
    """
    Generates a stream from frames.

        Parameters:
            camera (SpotCameras): instance of the SpotCameras class, connected to the robot's requested Image Service.
    """
    while True:
        frame = camera.get_frame()
        if (not frame):
            camera.__del__()
            break
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
