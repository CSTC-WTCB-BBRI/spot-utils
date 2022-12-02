# Copyright (c) 2022 Boston Dynamics, Inc.  All rights reserved.
#
# Downloading, reproducing, distributing or otherwise using the SDK Software
# is subject to the terms and conditions of the Boston Dynamics Software
# Development Kit License (20191101-BDSDK-SL).

# Some changes were made to only keep needed functionalities or add missing functionalities:
#   * Removed unused imports
#   * Removed unused functions and methods
#   * Added comments for code sections
#   * Added docstrings to functions
# See https://github.com/boston-dynamics/spot-sdk/blob/master/python/examples/estop/estop_nogui.py for the original file

#!/usr/bin/env python
"""Provides a programmatic estop to stop the robot."""


# Imports
import os
import sys
import time

## Boston Dynamics
import bosdyn.client.util
from bosdyn.client.estop import EstopEndpoint, EstopKeepAlive


# Main
class EstopNoGui():
    """Provides a software estop without a GUI.

    To use this estop, create an instance of the EstopNoGui class and use the stop() and allow()
    functions programmatically.
    """

    def __init__(self, client, timeout_sec, name=None):
        """
        Construct a new EstopNoGui instance

            Parameters:
                client (Client): Client for the Estop endpoint
                timeout_sec (int): Timeout of the new estop
                name (str): Estop endpoint name
        """

        # Force server to set up a single endpoint system
        ep = EstopEndpoint(client, name, timeout_sec)
        ep.force_simple_setup()

        # Begin periodic check-in between keep-alive and robot
        self.estop_keep_alive = EstopKeepAlive(ep)

    def stop(self):
        """
        Disallow the use of the robot
        """
        self.estop_keep_alive.stop()

    def allow(self):
        """
        Allow the use of the robot
        """
        self.estop_keep_alive.allow()
