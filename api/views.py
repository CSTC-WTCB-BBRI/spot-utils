#!/usr/bin/env python
"""Django views for the api application"""


# Imports
import os

## Django REST framework
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import StreamingHttpResponse, HttpResponse
from django.views.decorators import gzip

## Bosdyn
import bosdyn.client
from bosdyn.client.image import ImageClient

# Local imports
from .scripts.helloSpot import main
from .scripts.spot_cameras import gen, SpotCameras
from .scripts.gst_loopback_helper import GstLoopbackHelper
from .scripts.spot_cameras_image_service_helper import SpotCamerasImageServiceHelper

## Environment variables
from dotenv import load_dotenv
from manage import ROOT_DIR

load_dotenv(ROOT_DIR + '.env')

ROBOT_IP = os.getenv('ROBOT_IP')
GUID = os.getenv('GUID')
SECRET = os.getenv('SECRET')

# Logging
import logging
logger = logging.getLogger(__name__)

# Variables
camera = None
gstLoopbackHelper = None
spotCamerasImageServiceHelper = None


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
            {
                'Endpoint': '/camera/',
                'method': 'GET',
                'body': None,
                'description': 'Get live camera feed from Spot\'s cameras'
            },
            {
                'Endpoint': '/close-camera/',
                'method': 'GET',
                'body': None,
                'description': 'Close live camera feed from Spot\'s cameras'
            },
            {
                'Endpoint': '/start-gst-loopback',
                'method': 'GET',
                'body': None,
                'description': 'Execute gst_loopback for RICOH THETA'
            },
            {
                'Endpoint': '/stop-gst-loopback',
                'method': 'GET',
                'body': None,
                'description': 'Stop gst_loopback for RICOH THETA'
            },
            {
                'Endpoint': '/start-spot-cameras',
                'method': 'GET',
                'body': None,
                'description': 'Execute SpotCameras image service'
            },
            {
                'Endpoint': '/stop-spot-cameras',
                'method': 'GET',
                'body': None,
                'description': 'Stop SpotCameras image service'
            }
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
        main()
        return Response('Hello, Spot!')


@gzip.gzip_page
def getCameraFeed(request):
    """
    API endpoint for the camera live video feed
    """
    global camera
    if camera is not None:
        camera.__del__()
    # Create robot object with an image client.
    sdk = bosdyn.client.create_standard_sdk('image_capture')
    robot = sdk.create_robot(ROBOT_IP)
    robot.authenticate_from_payload_credentials(GUID, SECRET)
    robot.sync_with_directory()
    robot.time_sync.wait_for_sync()
    camera_request = request.GET.get('camera', 'frontleft_fisheye_image')
    if camera_request == "video99":
        image_client = robot.ensure_client("spot-cameras-image-service")
    else:
        image_client = robot.ensure_client(ImageClient.default_service_name)
    try :
        camera = SpotCameras(camera_request, image_client)
        return StreamingHttpResponse(gen(camera), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass

def closeCameraFeed(request):
    """
    API endpoint for closing the camera live video feed
    """
    global camera
    if camera is not None:
        camera.__del__()
    return HttpResponse()

def startSpotCamerasImageServiceView(request):
    """
    API endpoint for opening the RICOH THETA camera live video feed
    """
    global gstLoopbackHelper
    gstLoopbackHelper = GstLoopbackHelper()
    gstLoopbackHelper.start()
    logger.info('Starting GST Loopback')

    global spotCamerasImageServiceHelper
    spotCamerasImageServiceHelper = SpotCamerasImageServiceHelper()
    spotCamerasImageServiceHelper.start()
    logger.info('Starting SpotCameras service')

    return HttpResponse('Started SpotCameras image service on the robot.')

def stopSpotCamerasImageServiceView(request):
    """
    API endpoint for closing the RICOH THETA camera live video feed
    """
    global spotCamerasImageServiceHelper
    if spotCamerasImageServiceHelper is not None:
        logger.info('Stopping SpotCameras service')
        spotCamerasImageServiceHelper.stop()

    global gstLoopbackHelper
    if gstLoopbackHelper is not None:
        logger.info('Stopping GST Loopback')
        gstLoopbackHelper.stop()
    
    return HttpResponse('Stopped SpotCameras image service on the robot.')