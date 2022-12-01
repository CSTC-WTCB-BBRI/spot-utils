#!/usr/bin/env python
"""Django views for the api application"""


# Imports
import os

## Django REST framework
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from django.views.decorators import gzip

## Bosdyn
import bosdyn.client
from bosdyn.client.image import ImageClient

# Local imports
from .scripts.helloSpot import main as helloSpot
from .scripts.capture_laptop_frontcam_feed import gen, CaptureLaptop

## Environment variables
from dotenv import load_dotenv

load_dotenv('.env')
ROBOT_IP = os.getenv('ROBOT_IP')
GUID = os.getenv('GUID')
SECRET = os.getenv('SECRET')

# Variables
camera = None

# Main
class ApiRoutes(APIView):
    """
    API endpoint management
    """
    def get(self, request, format=None):
        """
        List all API endpoints
        """
        routes = [
            {
                'Endpoint': '/hello-spot/',
                'method': 'GET',
                'body': None,
                'description': 'Hello, Spot!'
            },
        ]
        return Response(routes)

class HelloSpot(APIView):
    """
    API endpoint for the HelloSpot functionality
    """
    def get(self, request, format=None):
        """
        Execute HelloSpot
        """
        helloSpot()
        return Response('Hello, Spot!')


@gzip.gzip_page
def getCameraFeed(request):
    """
    API endpoint for the camera live video feed
    """
    global camera
    # Create robot object with an image client.
    sdk = bosdyn.client.create_standard_sdk('image_capture')
    robot = sdk.create_robot(ROBOT_IP)
    robot.authenticate_from_payload_credentials(GUID, SECRET)
    robot.sync_with_directory()
    robot.time_sync.wait_for_sync()
    image_client = robot.ensure_client(ImageClient.default_service_name)
    try : 
        camera = CaptureLaptop(0, image_client)
        return StreamingHttpResponse(gen(camera), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass

def closeCameraFeed(request):
    """
    API endpoint for closing the camera live video feed
    """
    global camera
    camera.__del__()