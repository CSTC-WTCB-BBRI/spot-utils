#!/usr/bin/env python
"""Django urls for the main application"""


# Imports
from django.contrib import admin
from django.urls import path, include

# Main
"""
* /             ->      Link to the /web/urls.py file
* /admin/       ->      Link to the Django admin page
* /api/         ->      Link to the /api/urls.py file
"""
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('web.urls')),
    path('api/', include('api.urls')),
]