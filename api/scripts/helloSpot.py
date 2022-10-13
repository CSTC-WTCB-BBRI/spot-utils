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

    # The Boston Dynamics Python library uses Python's logging module to
    # generate output. Applications using the library can specify how
    # the logging information should be output.
    bosdyn.client.util.setup_logging(BOSDYN_CLIENT_LOGGING_VERBOSE)

    # Clients need to authenticate to a robot before being able to use it.
    bosdyn.client.util.authenticate(robot)

    # Establish time sync with the robot. This kicks off a background thread to establish time sync.
    # Time sync is required to issue commands to the robot. After starting time sync thread, block
    # until sync is established.
    robot.time_sync.wait_for_sync()

    # Verify the robot is not estopped and that an external application has registered and holds
    # an estop endpoint.
    assert not robot.is_estopped(), "Robot is estopped. Please use an external E-Stop client, " \
                                    "such as the estop SDK example, to configure E-Stop."

    # Only one client at a time can operate a robot. Clients acquire a lease to
    # indicate that they want to control a robot. Acquiring may fail if another
    # client is currently controlling the robot. When the client is done
    # controlling the robot, it should return the lease so other clients can
    # control it. The LeaseKeepAlive object takes care of acquiring and returning
    # the lease for us.
    lease_client = robot.ensure_client(bosdyn.client.lease.LeaseClient.default_service_name)
    with bosdyn.client.lease.LeaseKeepAlive(lease_client, must_acquire=True, return_at_exit=True):
        # Now, we are ready to power on the robot. This call will block until the power
        # is on. Commands would fail if this did not happen. We can also check that the robot is
        # powered at any point.
        robot.logger.info("Powering on robot... This may take several seconds.")
        robot.power_on(timeout_sec=20)
        assert robot.is_powered_on(), "Robot power on failed."
        robot.logger.info("Robot powered on.")

        # Tell the robot to stand up. The command service is used to issue commands to a robot.
        # The set of valid commands for a robot depends on hardware configuration. See
        # RobotCommandBuilder for more detailed examples on command building. The robot
        # command service requires timesync between the robot and the client.
        robot.logger.info("Commanding robot to stand...")
        command_client = robot.ensure_client(RobotCommandClient.default_service_name)
        blocking_stand(command_client, timeout_sec=10)
        robot.logger.info("Robot standing.")
        time.sleep(3)

        # Tell the robot to stand in a twisted position.
        #
        # The RobotCommandBuilder constructs command messages, which are then
        # issued to the robot using "robot_command" on the command client.
        #
        # In this example, the RobotCommandBuilder generates a stand command
        # message with a non-default rotation in the footprint frame. The footprint
        # frame is a gravity aligned frame with its origin located at the geometric
        # center of the feet. The X axis of the footprint frame points forward along
        # the robot's length, the Z axis points up aligned with gravity, and the Y
        # axis is the cross-product of the two.
        footprint_R_body = bosdyn.geometry.EulerZXY(yaw=0.4, roll=0.0, pitch=0.0)
        cmd = RobotCommandBuilder.synchro_stand_command(footprint_R_body=footprint_R_body)
        command_client.robot_command(cmd)
        robot.logger.info("Robot standing twisted.")
        time.sleep(3)

        # Now tell the robot to stand taller, using the same approach of constructing
        # a command message with the RobotCommandBuilder and issuing it with
        # robot_command.
        cmd = RobotCommandBuilder.synchro_stand_command(body_height=0.1)
        command_client.robot_command(cmd)
        robot.logger.info("Robot standing tall.")
        time.sleep(3)

        # Capture an image.
        # Spot has five sensors around the body. Each sensor consists of a stereo pair and a
        # fisheye camera. The list_image_sources RPC gives a list of image sources which are
        # available to the API client. Images are captured via calls to the get_image RPC.
        # Images can be requested from multiple image sources in one call.
        image_client = robot.ensure_client(ImageClient.default_service_name)
        sources = image_client.list_image_sources()
        image_response = image_client.get_image_from_sources(['frontleft_fisheye_image'])
        _maybe_display_image(image_response[0].shot.image)
        if config.save or config.save_path is not None:
            _maybe_save_image(image_response[0].shot.image, config.save_path)

        # Log a comment.
        # Comments logged via this API are written to the robots test log. This is the best way
        # to mark a log as "interesting". These comments will be available to Boston Dynamics
        # devs when diagnosing customer issues.
        log_comment = "HelloSpot tutorial user comment."
        robot.operator_comment(log_comment)
        robot.logger.info('Added comment "%s" to robot log.', log_comment)

        # Power the robot off. By specifying "cut_immediately=False", a safe power off command
        # is issued to the robot. This will attempt to sit the robot before powering off.
        robot.power_off(cut_immediately=False, timeout_sec=20)
        assert not robot.is_powered_on(), "Robot power off failed."
        robot.logger.info("Robot safely powered off.")

def getSpotAuthentication():
    return BOSDYN_CLIENT_USERNAME, BOSDYN_CLIENT_PASSWORD

def main():
    # Create robot object
    sdk = bosdyn.client.create_standard_sdk(CLIENT_NAME)
    robot = sdk.create_robot(ROBOT_IP)
    bosdyn.client.util.authenticate(robot, getSpotAuthentication())

    # Create estop client for the robot
    estop_client = robot.ensure_client(EstopClient.default_service_name)

    # Create nogui estop
    estop_nogui = EstopNoGui(estop_client, ROBOT_ESTOP_TIMEOUT_SEC, "Estop NoGUI")

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
