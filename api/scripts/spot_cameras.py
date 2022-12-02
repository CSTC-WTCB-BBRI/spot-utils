import numpy as np
from scipy import ndimage
import cv2 as cv

import bosdyn.client
from bosdyn.api import image_pb2

ROTATION_ANGLE = {
    'back_fisheye_image': 0,
    'frontleft_fisheye_image': -90,
    'frontright_fisheye_image': -90,
    'left_fisheye_image': 0,
    'right_fisheye_image': 180
}

class SpotCameras(object):

    def __init__(self, camera_index, image_client):
        self.cameras = {
            'back_fisheye_image': 'back_fisheye_image',
            'frontleft_fisheye_image': 'frontleft_fisheye_image',
            'frontright_fisheye_image': 'frontright_fisheye_image',
            'left_fisheye_image': 'left_fisheye_image',
            'right_fisheye_image': 'right_fisheye_image'
        }
        self.frame = None
        self.image_client = image_client
        self.getImage()
    
    def getImage(self):
        image_responses = self.image_client.get_image_from_sources([self.cameras['frontleft_fisheye_image']])
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
        frame = self.frame
        try:
            _, jpeg = cv.imencode('.jpg', frame)
            return jpeg.tobytes()
        except:
            return False
