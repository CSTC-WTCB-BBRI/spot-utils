#!/usr/bin/env python
"""Helper for starting/stopping the SpotCameras Image Service"""

# Imports
import subprocess
import time
import os

# Local imports
## Environment variables
from dotenv import load_dotenv
from manage import ROOT_DIR

load_dotenv(ROOT_DIR + '.env')

ROBOT_IP = os.getenv('ROBOT_IP')
ROBOT_USERNAME = os.getenv('ROBOT_USERNAME')
ROBOT_SSH_PORT = eval(os.getenv('ROBOT_SSH_PORT'))
ROBOT_SPOT_UTILS_ROOT_DIR = os.getenv('ROBOT_SPOT_UTILS_ROOT_DIR')

# Main
class SpotCamerasImageServiceHelper(object):
    """
    Helper class for the SpotCameras Image Service.
    """
    def __init__(self):
        """
        Construct a new SpotCamerasImageServiceHelper instance by connecting to the Spot CORE.
        """
        self.sshProc = subprocess.Popen(f"ssh -o StrictHostKeyChecking=no -tt {ROBOT_USERNAME}@{ROBOT_IP} -p {ROBOT_SSH_PORT}",
                               shell=True,
                               stdin=subprocess.PIPE, 
                               stdout = subprocess.PIPE,
                               universal_newlines=True,
                               bufsize=0)
    
    def start(self):
        """
        Starts the SpotCameras Image Service
        """
        cmd1 = "cd " + ROBOT_SPOT_UTILS_ROOT_DIR + "/spot-services/SpotCameras\n"
        self.sshProc.stdin.write(cmd1)
        cmd2 = "docker-compose up -d\n"
        self.sshProc.stdin.write(cmd2)

    def stop(self):
        """
        Stops the SpotCameras Image Service
        """
        cmd1 = "cd " + ROBOT_SPOT_UTILS_ROOT_DIR + "/spot-services/SpotCameras\n"
        self.sshProc.stdin.write(cmd1)
        cmd2 = "docker-compose down\n"
        self.sshProc.stdin.write(cmd2)
        self.sshProc.stdin.close()
