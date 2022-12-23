#!/usr/bin/env python
"""Helper for starting/stopping the gst_loopback script"""


# Imports
import subprocess
import time
import signal
import os

# Local imports
## Environment variables
from dotenv import load_dotenv
from manage import ROOT_DIR

load_dotenv(ROOT_DIR + '.env')

ROBOT_IP = os.getenv('ROBOT_IP')
ROBOT_USERNAME = os.getenv('ROBOT_USERNAME')
ROBOT_SSH_PORT = eval(os.getenv('ROBOT_SSH_PORT'))
ROBOT_LIBUVC_THETA_SAMPLE_ROOT_DIR = os.getenv('ROBOT_LIBUVC_THETA_SAMPLE_ROOT_DIR')

# Main
class GstLoopbackHelper(object):
    """
    Helper class for the gst_loopback script.
    """
    def __init__(self):
        """
        Construct a new GstLoopbackHelper instance by connecting to the Spot CORE.
        """
        self.sshProc = subprocess.Popen(f"ssh -tt {ROBOT_USERNAME}@{ROBOT_IP} -p {ROBOT_SSH_PORT}",
                               shell=True,
                               stdin=subprocess.PIPE, 
                               stdout = subprocess.PIPE,
                               universal_newlines=True,
                               bufsize=0)
    
    def start(self):
        """
        Starts the gst_loopback script
        """
        cmd = ROBOT_LIBUVC_THETA_SAMPLE_ROOT_DIR + "gst/gst_loopback\n"
        self.sshProc.stdin.write(cmd)
    
    def stop(self):
        """
        Stops the gst_loopback script
        """
        self.sshProc.stdin.write("\n")
        self.sshProc.stdin.write("exit\n")
        self.sshProc.stdin.close()
