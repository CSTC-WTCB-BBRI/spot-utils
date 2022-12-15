#!/usr/bin/env python
"""Django views for the web application"""


# Imports
from django.shortcuts import render

## Django REST framework
from rest_framework.views import APIView


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
    def get(self, request, format=None):
        """
        Get the Pointcloud web page
        """
        return render(request, 'web/pointcloud.html', {})
