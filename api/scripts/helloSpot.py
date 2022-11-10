from estop_nogui import EstopNoGui

import bosdyn.client.util
from bosdyn.client.estop import EstopClient, EstopEndpoint, EstopKeepAlive
from bosdyn.client.robot_state import RobotStateClient

import argparse
import os
import sys

from dotenv import load_dotenv
load_dotenv()

ROBOT_IP = os.getenv('ROBOT_IP')
CLIENT_NAME = os.getenv('CLIENT_NAME')
ROBOT_ESTOP_TIMEOUT_SEC = os.getenv('ROBOT_ESTOP_TIMEOUT_SEC')
BOSDYN_CLIENT_LOGGING_VERBOSE = os.getenv('BOSDYN_CLIENT_LOGGING_VERBOSE')
BOSDYN_CLIENT_USERNAME = os.getenv('BOSDYN_CLIENT_USERNAME')
BOSDYN_CLIENT_PASSWORD = os.getenv('BOSDYN_CLIENT_PASSWORD')

def hello_spot(robot):
    """A simple example of using the Boston Dynamics API to command a Spot robot."""

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

        # Power the robot off
        robot.power_off(cut_immediately=False, timeout_sec=20)
        assert not robot.is_powered_on(), "Robot power off failed."
        robot.logger.info("Robot safely powered off.")

def getSpotAuthentication():
    ## TO DO
    ## IMPLEMENT AUTHENTICATION MECHANISM
    return BOSDYN_CLIENT_USERNAME, BOSDYN_CLIENT_PASSWORD

def main():
    # Setup logging
    bosdyn.client.util.setup_logging(BOSDYN_CLIENT_LOGGING_VERBOSE)
    
    # Create robot object
    sdk = bosdyn.client.create_standard_sdk(CLIENT_NAME)
    robot = sdk.create_robot(ROBOT_IP)
    bosdyn.client.util.authenticate(robot, getSpotAuthentication())

    # Create estop client for the robot
    estop_client = robot.ensure_client(EstopClient.default_service_name)

    # Create nogui estop
    estop_nogui = EstopNoGui(estop_client, ROBOT_ESTOP_TIMEOUT_SEC, "Estop NoGUI")
    estop_nogui.allow()

    # Create robot state client for the robot
    state_client = robot.ensure_client(RobotStateClient.default_service_name)

    try:
        hello_spot(robot)
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
