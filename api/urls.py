#!/usr/bin/env python
"""Django urls for the api application"""


# Imports
from django.urls import path

# Local imports
from .views import ApiRoutes, HelloSpot, getCameraFeed, closeCameraFeed, startGstLoopbackView, stopGstLoopbackView, startSpotCamerasImageServiceView, stopSpotCamerasImageServiceView


# Main
"""
* /api/                         ->      List all API endpoints
* /api/hello-spot/              ->      Execute HelloSpot
* /api/camera/                  ->      Get live camera feed
* /api/close-camera             ->      Close live camera feed
* /api/start-gst-loopback       ->      Execute gst_loopback
* /api/stop-gst-loopback        ->      Stop gst_loopback
* /api/start-spot-camera        ->      Run SpotCameras image service
* /api/stop-spot-camera         ->      Stop SpotCameras image service
"""
urlpatterns = [
    path('', ApiRoutes.as_view(), name='api-routes'),
    path('hello-spot/', HelloSpot.as_view(), name='api-hello-spot'),
    path('camera/', getCameraFeed, name='api-get-camera-feed'),
    path('close-camera/', closeCameraFeed, name='api-close-camera'),
    path('start-gst-loopback/', startGstLoopbackView, name='api-start-gst-loopback'),
    path('stop-gst-loopback/', stopGstLoopbackView, name='api-stop-gst-loopback'),
    path('start-spot-cameras/', startSpotCamerasImageServiceView, name='api-start-spot-cameras'),
    path('stop-spot-cameras/', stopSpotCamerasImageServiceView, name='api-stop-spot-cameras'),
]