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
#   * Included call to EstopNoGui (no need to setup an Estop prior to this script execution) within the main function
#   * Included a getSpotAuthentication function to authenticate user on Spot 
#   * Added instruction to sit before shutting down in the hello_spot function
#   * Removed the 'Capture an image' instruction
#   * Added a state_client argument to the hello_spot function
# See https://github.com/boston-dynamics/spot-sdk/blob/master/python/examples/hello_spot/hello_spot.py for the original file

#!/usr/bin/env python
"""Orders spot to execute a series of basic commands"""


# Imports
import os
import sys
import time

from dotenv import load_dotenv

## Boston Dynamics
import bosdyn.client.util
from bosdyn.client.estop import EstopClient
from bosdyn.client.robot_state import RobotStateClient
from bosdyn.client.robot_command import RobotCommandBuilder, RobotCommandClient, blocking_stand

# Local imports
from .estop_nogui import EstopNoGui

## Environment variables
load_dotenv()

ROBOT_IP = os.getenv('ROBOT_IP')
CLIENT_NAME = os.getenv('CLIENT_NAME')
ROBOT_ESTOP_TIMEOUT_SEC = os.getenv('ROBOT_ESTOP_TIMEOUT_SEC')
BOSDYN_CLIENT_LOGGING_VERBOSE = os.getenv('BOSDYN_CLIENT_LOGGING_VERBOSE')
BOSDYN_CLIENT_USERNAME = os.getenv('BOSDYN_CLIENT_USERNAME')
BOSDYN_CLIENT_PASSWORD = os.getenv('BOSDYN_CLIENT_PASSWORD')


# Main
def hello_spot(robot, state_client):
    """
    A simple example of using the Boston Dynamics API to command a Spot robot.

        Parameters:
            robot (Robot): robot instance
            state_client (Client): Client for the robot state
    """

    # Establish time sync with the robot
    robot.time_sync.wait_for_sync()
    
    # Check robot is not estopped
    assert not robot.is_estopped(), "Robot is estopped. Please use an external E-Stop client, " \
                                    "such as the estop SDK example, to configure E-Stop."

    # Acquire lease
    lease_client = robot.ensure_client(bosdyn.client.lease.LeaseClient.default_service_name)
    with bosdyn.client.lease.LeaseKeepAlive(lease_client, must_acquire=True, return_at_exit=True):
        # Power on the robot
        robot.logger.info("Powering on robot... This may take several seconds.")
        robot.power_on(timeout_sec=20)
        assert robot.is_powered_on(), "Robot power on failed."
        robot.logger.info("Robot powered on.")
        time.sleep(5)

        # Command the robot to stand up
        robot.logger.info("Commanding robot to stand...")
        command_client = robot.ensure_client(RobotCommandClient.default_service_name)
        blocking_stand(command_client, timeout_sec=10)
        robot.logger.info("Robot standing.")
        time.sleep(3)

        # Command the robot to stand in a twisted position.
        footprint_R_body = bosdyn.geometry.EulerZXY(yaw=0.4, roll=0.0, pitch=0.0)
        cmd = RobotCommandBuilder.synchro_stand_command(footprint_R_body=footprint_R_body)
        command_client.robot_command(cmd)
        robot.logger.info("Robot standing twisted.")
        time.sleep(3)

        # Command the robot to stand taller
        cmd = RobotCommandBuilder.synchro_stand_command(body_height=0.1)
        command_client.robot_command(cmd)
        robot.logger.info("Robot standing tall.")
        time.sleep(3)

        # Log a comment
        log_comment = "HelloSpot tutorial user comment."
        robot.operator_comment(log_comment)
        robot.logger.info('Added comment "%s" to robot log.', log_comment)

        # Sit the robot down
        robot.logger.info("Commanding robot to sit...")
        cmd = RobotCommandBuilder.sit_command()
        command_client.robot_command(cmd)
        robot.logger.info("Robot ssitting.")
        time.sleep(3)

        # Power the robot off
        robot.power_off(cut_immediately=False, timeout_sec=20)
        assert not robot.is_powered_on(), "Robot power off failed."
        robot.logger.info("Robot safely powered off.")

def getSpotAuthentication():
    """
    Provide authentication to Spot

        Returns:
            BOSDYN_CLIENT_USERNAME (str): username
            BOSDYN_CLIENT_PASSWORD (str): password
    """
    ## TO DO
    ## IMPLEMENT AUTHENTICATION MECHANISM
    return BOSDYN_CLIENT_USERNAME, BOSDYN_CLIENT_PASSWORD

def main():
    """
    Sets up the robot for executing HelloSpot

        Returns:
            (boolean): The function execution was successful (or not)
        
        Raises:
            Exception: Hello, Spot! threw an exception
    """
    # Setup logging
    bosdyn.client.util.setup_logging(BOSDYN_CLIENT_LOGGING_VERBOSE)
    
    # Create robot object
    sdk = bosdyn.client.create_standard_sdk(CLIENT_NAME)
    robot = sdk.create_robot(ROBOT_IP)
    bosdyn.client.util.authenticate(robot, getSpotAuthentication())

    # Create estop client for the robot
    estop_client = robot.ensure_client(EstopClient.default_service_name)

    # Create nogui estop
    estop_nogui = EstopNoGui(estop_client, int(ROBOT_ESTOP_TIMEOUT_SEC), "Estop NoGUI")
    estop_nogui.allow()

    # Create robot state client for the robot
    state_client = robot.ensure_client(RobotStateClient.default_service_name)

    try:
        hello_spot(robot, state_client)
        estop_nogui.stop()
        return True
    except Exception as exc:  # pylint: disable=broad-except
        logger = bosdyn.client.util.get_logger()
        logger.error("Hello, Spot! threw an exception: %r", exc)
        estop_nogui.stop()
        return False

if __name__ == '__main__':
    if not main():
        sys.exit(1)
