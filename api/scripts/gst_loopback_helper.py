#!/usr/bin/env python
"""Helper for starting/stopping the gst_loopback script"""


# Imports
import subprocess
import os

# Local imports
## Environment variables
from dotenv import load_dotenv
from manage import ROOT_DIR

load_dotenv(ROOT_DIR + '.env')

DEV_MODE = os.getenv('DEV_MODE')
ROBOT_IP = os.getenv('ROBOT_IP')
ROBOT_USERNAME = os.getenv('ROBOT_USERNAME')
ROBOT_SSH_PORT = eval(os.getenv('ROBOT_SSH_PORT'))
ROBOT_LIBUVC_THETA_SAMPLE_ROOT_DIR = os.getenv('ROBOT_LIBUVC_THETA_SAMPLE_ROOT_DIR')

# Logging
import logging
logger = logging.getLogger(__name__)

# Main
class GstLoopbackHelper(object):
    """
    Helper class for the gst_loopback script.
    """
    def __init__(self):
        """
        Construct a new GstLoopbackHelper instance by connecting to the Spot CORE.
        """
        if DEV_MODE == "True":
            self.proc = subprocess.Popen(f"ssh -o StrictHostKeyChecking=no -tt {ROBOT_USERNAME}@{ROBOT_IP} -p {ROBOT_SSH_PORT}",
                               shell=True,
                               stdin=subprocess.PIPE, 
                               stdout=subprocess.PIPE,
                               universal_newlines=True,
                               bufsize=0)
        else:
            self.proc = subprocess.Popen(f"bash",
                               shell=True,
                               stdin=subprocess.PIPE, 
                               stdout=subprocess.PIPE,
                               universal_newlines=True,
                               bufsize=0)
    
    def start(self):
        """
        Starts the gst_loopback script
        """
        cmd = ROBOT_LIBUVC_THETA_SAMPLE_ROOT_DIR + "/gst/gst_loopback\n"
        self.proc.stdin.write(cmd)
    
    def stop(self):
        """
        Stops the gst_loopback script
        """
        self.proc.stdin.write("\n")
        self.proc.stdin.write("exit\n")
        self.proc.stdin.close()
