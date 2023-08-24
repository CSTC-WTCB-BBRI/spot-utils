#!/usr/bin/env python
"""
Allows generating new pointclouds
Created on Fri Dec  9 16:50:05 2022
@author: tlo

edited by Nicolas Daxhelet
  * removed unused functionalities (in the context of spot-utils)
  * removed comments and `print` lines
  * reorganised functionalities in a Python class with methods
  * added use of env variables
"""

# Imports
import requests
import os

# Local imports
## Environment variables
from dotenv import load_dotenv
from manage import ROOT_DIR

load_dotenv(ROOT_DIR + '.env')

ROBOT_IP = os.getenv('ROBOT_IP')
SPOT_SLAM_PORT = os.getenv('SPOT_SLAM_PORT')

# Variables
url = f"http://{ROBOT_IP}:{SPOT_SLAM_PORT}"

# Main
class SpotSLAMHelper(object):
    """
    Helper class for interacting with the Spot-SLAM payload and generating new pointclouds
    """
    ready_to_export = False

    def launch(self):
        """
        Construct a new SpotSLAMHelper instance by connecting to Spot,
          making sure the Spot-SLAM docker instance is started.
        """
        requests.get(url + "/launch")
    
    def authorize(self):
        """
        Authorize the Spot-SLAM payload to acces the LiDAR on the robot.
        """
        requests.get(url + "/connect2Spot")
    
    def start(self):
        """
        Start capturing LiDAR data with Spot-SLAM.
        """
        requests.get(url + "/start_slam")
    
    def stop(self):
        """
        Stop capturing LiDAR data with Spot-SLAM.
        """
        requests.get(url + "/stop_slam")
        self.ready_to_export = True
    
    def save(self):
        """
        Export captured LiDAR data in PCD pointcloud format.
        """
        requests.get(url + "/save_map_slam/")
    
    def potree(self):
        """
        Export PCD pointcloud format to potree pointcloud format.
        """
        requests.get(url + "/potree")
