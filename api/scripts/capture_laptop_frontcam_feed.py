import numpy as np
import cv2 as cv
import threading

class CaptureLaptop(object):

    def __init__(self, camera_index):
        self.video = cv.VideoCapture(camera_index)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()
    
    def __del__(self):
        self.video.release()

    def get_frame(self):
        frame = self.frame
        try:
            _, jpeg = cv.imencode('.jpg', frame)
            return jpeg.tobytes()
        except:
            return False
    
    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    while True:
        frame = camera.get_frame()
        if (not frame):
            camera.__del__()
            break
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
