#!/usr/bin/env python
"""Django views for the web application"""


# Imports
from django.shortcuts import render

## Django REST framework
from rest_framework.views import APIView

# Local Imports
from api.scripts.available_pointclouds_helper import AvailablePointcloudsHelper

# Main
class Auth(APIView):
    """
    Authentication web page management
    """
    def get(self, request, format=None):
        """
        Get the Authentication web page
        """
        return render(request, 'web/auth.html', {})

class Dashboard(APIView):
    """
    Dashboard web page management
    """
    def get(self, request, format=None):
        """
        Get the Dashboard web page
        """
        return render(request, 'web/dashboard.html', {})

class Pointcloud(APIView):
    """
    Pointcloud web page management
    """
    def get(self, request, name, format=None):
        """
        Get the Pointcloud web page
        """
        return render(request, 'web/pointcloud.html', { 'name': name })

class PointcloudIndex(APIView):
    """
    Pointcloud index web page
    """
    def get(self, request, format=None):
        """
        Get the list of available Pointclouds
        """
        helper = AvailablePointcloudsHelper()
        pointclouds = helper.list()
        context = { 'pointclouds': pointclouds }
        return render(request, 'web/pointcloud_index.html', context)
