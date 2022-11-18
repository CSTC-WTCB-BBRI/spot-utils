#!/usr/bin/env python
"""Django views for the api application"""


# Imports
## Django REST framework
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from django.views.decorators import gzip

# Local imports
from .scripts.helloSpot import main as helloSpot
from .scripts.capture_laptop_frontcam_feed import gen, CaptureLaptop

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
    try : 
        camera = CaptureLaptop(0)
        return StreamingHttpResponse(gen(camera), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass

def closeCameraFeed(request):
    """
    API endpoint for closing the camera live video feed
    """
    global camera
    camera.__del__()