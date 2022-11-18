#!/usr/bin/env python
"""Django urls for the web application"""


# Imports
from django.urls import path

# Local imports
from .views import Auth, Dashboard, Pointcloud


# Main
"""
* /             ->      Get the Dashboard web page
* /auth/        ->      Get the Authentication web page
* /pointcloud/  ->      Get the Pointcloud web page
"""
urlpatterns = [
    path('auth', Auth.as_view(), name='web-auth'),
    path('', Dashboard.as_view(), name='web-dashboard'),
    path('pointcloud', Pointcloud.as_view(), name='web-pointcloud'),
]