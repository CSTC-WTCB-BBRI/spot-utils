#!/usr/bin/env python
"""Django urls for the api application"""


# Imports
from django.urls import path

# Local imports
from .views import ApiRoutes, HelloSpot, getCameraFeed, closeCameraFeed


# Main
"""
* /api/             ->      List all API endpoints
* /api/hello-spot/  ->      Execute HelloSpot
* /api/camera/      ->      Get live camera feed
"""
urlpatterns = [
    path('', ApiRoutes.as_view(), name='api-routes'),
    path('hello-spot/', HelloSpot.as_view(), name='api-hello-spot'),
    path('camera/', getCameraFeed, name='api-get-camera-feed'),
    path('close-camera/', closeCameraFeed, name='api-close-camera'),
]