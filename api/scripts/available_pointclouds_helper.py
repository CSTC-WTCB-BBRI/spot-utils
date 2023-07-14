#!/usr/bin/env python
"""Helper for the available pointclouds"""


# Imports
import os

# Local imports
## Environment variables
from dotenv import load_dotenv
from manage import ROOT_DIR

load_dotenv(ROOT_DIR + '.env')

# Logging
import logging
logger = logging.getLogger(__name__)

# Main
class AvailablePointcloudsHelper(object):
    """
    Helper class for available pointclouds.
    """
    def __init__(self):
        """
        Construct a new AvailablePointcloudsHelper instance by making an inventory
        of the current content of the /staticfiles/pointclouds directory.
        """
        self.pointclouds_dir = os.path.join(ROOT_DIR, 'staticfiles', 'data')
        self.pointclouds = self._get_available_pointclouds()

    def _get_available_pointclouds(self):
        """
        Helper method to retrieve the list of available pointclouds in the directory.
        """
        pointclouds = []
        if os.path.exists(self.pointclouds_dir) and os.path.isdir(self.pointclouds_dir):
            for entry in os.scandir(self.pointclouds_dir):
                if entry.is_dir() and entry.name.startswith('spot'):
                    pointclouds.append(entry.name)
        return pointclouds
    
    def list(self):
        """
        Outputs the list of available pointclouds.
        """
        pass

    def collect_new_pointclouds(self):
        """
        Executes the `collectstatic` function to refresh the list of available pointclouds.
        """
        pass