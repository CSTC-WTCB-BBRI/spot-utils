import numpy as np
import cv2 as cv
import threading

#########################

# TO DO
# REMOVE USELESS IMPORTS

#########################

import argparse
import sys
import os

import cv2
import numpy as np
from scipy import ndimage

import bosdyn.client
import bosdyn.client.util
from bosdyn.api import image_pb2
from bosdyn.client.image import ImageClient, build_image_request

## Environment variables
from dotenv import load_dotenv

load_dotenv('.env')

GUID = os.getenv('GUID')
SECRET = os.getenv('SECRET')
ROBOT_IP = os.getenv('ROBOT_IP')

class CaptureLaptop(object):

    def __init__(self, camera_index, image_client):
        self.frame = None
        self.image_client = image_client
        self.getImage()
        self.updating = True
        threading.Thread(target=self.update, args=()).start()
    
    def __del__(self):
        self.updating = False
    
    def getImage(self):
        image_responses = self.image_client.get_image_from_sources(['frontleft_fisheye_image'])
        image = image_responses[0]
        num_bytes = 1  # Assume a default of 1 byte encodings.
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
                img = cv2.imdecode(img, -1)
        else:
            img = cv2.imdecode(img, -1)
        self.frame = img


    def get_frame(self):
        frame = self.frame
        try:
            _, jpeg = cv.imencode('.jpg', frame)
            return jpeg.tobytes()
        except:
            return False
    
    def update(self):
        while self.updating:
            self.getImage()

def gen(camera):
    while True:
        frame = camera.get_frame()
        if (not frame):
            camera.__del__()
            break
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
