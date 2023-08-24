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

import json

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
    def launch(self):
        """
        Construct a new SpotSLAMHelper instance by connecting to Spot,
          making sure the Spot-SLAM docker instance is started.
        """
        ret = requests.get(url + "/launch", verify=False)
        return json.dumps(json.loads(ret.content)['msg'], indent=2)
    
    def authorize(self):
        """
        Authorize the Spot-SLAM payload to acces the LiDAR on the robot.
        """
        ret = requests.get(url + "/connect2Spot", verify=False)
        return json.dumps(json.loads(ret.content)['msg'], indent=2)
    
    def start(self):
        """
        Start capturing LiDAR data with Spot-SLAM.
        """
        ret = requests.get(url + "/start_slam", verify=False)
        return json.dumps(json.loads(ret.content)['msg'], indent=2)
    
    def stop(self):
        """
        Stop capturing LiDAR data with Spot-SLAM.
        """
        ret = requests.get(url + "/stop_slam", verify=False)
        return json.loads(ret.content)['msg']
    
    def save(self):
        """
        Export captured LiDAR data in PCD pointcloud format.
        """
        ret = requests.get(url + "/save_map_slam/", verify=False)
        return json.dumps(json.loads(ret.content)['msg'], indent=2)
    
    def potree(self):
        """
        Export PCD pointcloud format to potree pointcloud format.
        """
        ret = requests.get(url + "/potree", verify=False)
        return json.dumps(json.loads(ret.content)['msg'], indent=2)
