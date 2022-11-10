#!/usr/bin/env python
"""Django views for the api application"""


# Imports
## Django REST framework
from rest_framework.views import APIView
from rest_framework.response import Response

# Local imports
from .scripts.helloSpot import main


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
        main()
        return Response('Hello, Spot!')