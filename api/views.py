#!/usr/bin/env python
"""Django views for the api application"""


# Imports
import os

## Django REST framework
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import StreamingHttpResponse, HttpResponse
from django.views.decorators import gzip
from django.views.decorators.http import require_http_methods

## Bosdyn
import bosdyn.client
from bosdyn.client.image import ImageClient

# Local imports
from .decorators import require_get, require_delete
from .scripts.helloSpot import main
from .scripts.spot_cameras import gen, SpotCameras
from .scripts.gst_loopback_helper import GstLoopbackHelper
from .scripts.spot_cameras_image_service_helper import SpotCamerasImageServiceHelper
from .scripts.available_pointclouds_helper import AvailablePointcloudsHelper
from .scripts.spot_slam import SpotSLAMHelper

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
                'endpoint': '/hello-spot/',
                'method': 'GET',
                'body': None,
                'description': 'Hello, Spot!'
            },
            {
                'endpoint': '/camera/',
                'method': 'GET',
                'body': None,
                'description': 'Get live camera feed from Spot\'s cameras'
            },
            {
                'endpoint': '/close-camera/',
                'method': 'DELETE',
                'body': None,
                'description': 'Close live camera feed from Spot\'s cameras'
            },
            {
                'endpoint': '/start-spot-cameras',
                'method': 'GET',
                'body': None,
                'description': 'Execute SpotCameras image service'
            },
            {
                'endpoint': '/stop-spot-cameras',
                'method': 'DELETE',
                'body': None,
                'description': 'Stop SpotCameras image service'
            },
            {
                'endpoint': '/pointclouds',
                'method': 'GET',
                'body': None,
                'description': 'List available services'
            },
            {
                'endpoint': '/pointclouds',
                'method': 'POST',
                'body': None,
                'description': 'Collect new pointclouds'
            },
            {
                'endpoint': '/spot-slam?slam=start',
                'method': 'POST',
                'body': None,
                'description': 'Start LiDAR data collection'
            },
            {
                'endpoint': '/spot-slam?slam=stop',
                'method': 'POST',
                'body': None,
                'description': 'Stop LiDAR data collection'
            },
            {
                'endpoint': '/spot-slam?slam=start',
                'method': 'POST',
                'body': None,
                'description': 'Export LiDAR data to potree pointcloud format'
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

@require_get
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

@require_delete
def closeCameraFeed(request):
    """
    API endpoint for closing the camera live video feed
    """
    global camera
    if camera is not None:
        camera.__del__()
    return HttpResponse()

@require_get
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

@require_delete
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

class Pointclouds(APIView):
    """
    API endpoint for pointcloud management
    """
    def get(self, request, format=None):
        """
        List available pointclouds (in the `/staticfiles/pointclouds` directory)
        """
        pointclouds = [
            {
                'name': 'pointcloud1',
                'date': '13.07.2023'
            },
            {
                'name': 'pointcloud2',
                'date': '14.07.2023'
            },
        ]
        return Response(pointclouds)
    
    def post(self, request, format=None):
        """
        Collect new pointclouds placed in the data folder.
        """
        helper = AvailablePointcloudsHelper()
        return HttpResponse(helper.collect_new_pointclouds())
    
class SpotSLAM(APIView):
    """
    API endpoint for generating new pointclouds
    """
    def post(self, request, format=None):
        """
        Endpoint disambiguation.
        """
        slam_request = request.GET.get('slam', 'start')
        if slam_request == "start":
            return Response(self._start())
        elif slam_request == "export":
            return Response(self._export())
        else:
            return Response(self._stop())
        
    def _start(self):
        """
        Start collecting LiDAR data with Spot-SLAM.
        """
        helper = SpotSLAMHelper()
        ret_launch = helper.launch()
        ret_auth = helper.authorize()
        ret_start = helper.start()
        return ret_launch + "##SEP##" + ret_auth + "##SEP##" + ret_start
    
    def _stop(self):
        """
        Stop collecting LiDAR data with Spot-SLAM.
        """
        helper = SpotSLAMHelper()
        ret_stop = helper.stop()
        return ret_stop
        
    def _export(self):
        """
        Export collected LiDAR data to potree pointcloud format.
        """
        helper = SpotSLAMHelper()
        ret_save = helper.save()
        ret_potree = helper.potree()
        return ret_save + "###SEP###" + ret_potree
    