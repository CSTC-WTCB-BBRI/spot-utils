#!/usr/bin/env python
"""Tests for the HelloSpot python script"""

# Imports
import mock

## Bosdyn
from bosdyn.client.directory import DirectoryClient
from bosdyn.client.time_sync import TimeSyncClient
from bosdyn.client.lease import LeaseClient
from bosdyn.client.power import PowerClient
from bosdyn.client.robot import Robot
from bosdyn.client.robot_state import RobotStateClient
from bosdyn.client.robot_command import RobotCommandClient

## Django
from django.test import TestCase

# Local imports
from api.scripts import helloSpot


# Main
class HelloSpotTestCase(TestCase):
    """
    Test cases for the HelloSpot python script.
    """
    robot = None
    state_client = None

    def mocked_creation_function_for_directory_service(self):
        directoryClient = DirectoryClient()
        directoryClient.authority = 'mockedAuthority'
        return directoryClient

    def mocked_creation_function_for_time_sync_service(self):
        timeSyncClient = TimeSyncClient()
        timeSyncClient.authority = 'mockedAuthority'
        return timeSyncClient

    def mocked_creation_function_for_lease_service(self):
        leaseClient = LeaseClient()
        leaseClient.authority = 'mockedAuthority'
        return leaseClient

    def mocked_creation_function_for_power_service(self):
        powerClient = PowerClient()
        powerClient.authority = 'mockedAuthority'
        return powerClient

    def mocked_creation_function_for_robot_state_service(self):
        robotStateClient = RobotStateClient()
        robotStateClient.authority = 'mockedAuthority'
        return robotStateClient

    def mocked_creation_function_for_robot_command_service(self):
        robotCommandClient = RobotCommandClient()
        robotCommandClient.authority = 'mockedAuthority'
        return robotCommandClient

    def setUp(self):
        """
        This method is ran before each test case in this class.
            Initialisation of a new Robot instance.
        """
        self.robot = Robot(name='MockSpot')
        self.robot.service_type_by_name['time-sync'] = 'mockTimeSyncServiceType'
        self.robot.service_type_by_name['directory'] = 'mockDirectoryServiceType'
        self.robot.service_type_by_name['lease'] = 'mockLeaseServiceType'
        self.robot.service_type_by_name['power'] = 'mockPowerServiceType'
        self.robot.service_type_by_name['robot-state'] = 'mockRobotStateServiceType'
        self.robot.service_type_by_name['robot-command'] = 'mockRobotCommandServiceType'
        self.robot.service_client_factories_by_type['mockTimeSyncServiceType'] = self.mocked_creation_function_for_time_sync_service
        self.robot.service_client_factories_by_type['mockDirectoryServiceType'] = self.mocked_creation_function_for_directory_service
        self.robot.service_client_factories_by_type['mockLeaseServiceType'] = self.mocked_creation_function_for_lease_service
        self.robot.service_client_factories_by_type['mockPowerServiceType'] = self.mocked_creation_function_for_power_service
        self.robot.service_client_factories_by_type['mockRobotStateServiceType'] = self.mocked_creation_function_for_robot_state_service
        self.robot.service_client_factories_by_type['mockRobotCommandServiceType'] = self.mocked_creation_function_for_robot_command_service

    def mocked_robot_call(self, rpc_method, request, value_from_response=None, error_from_response=None, copy_request=True, **kwargs):
        service = dict()
        return [service]

    def mocked_sync_with_services_list(self, service_list):
        self.authorities_by_name['time-sync'] = 'mockedAuthority'
        self.authorities_by_name['directory'] = 'mockedAuthority'
        self.authorities_by_name['lease'] = 'mockedAuthority'
        self.authorities_by_name['power'] = 'mockedAuthority'
        self.authorities_by_name['robot-state'] = 'mockedAuthority'
        self.authorities_by_name['robot-command'] = 'mockedAuthority'
        return self.service_type_by_name
    
    def mocked_wait_for_sync(self, timeout_sec=3.0):
        return

    def mocked_is_estopped(self, timeout=None):
        return False
    
    def mocked_power_command(power_client, request, timeout_sec=30, update_frequency=1.0, expect_grpc_timeout=False, **kwargs):
        return
    
    def mocked_is_powered_on(state_client, **kwargs):
        return True
    
    def mocked_blocking_stand(command_client, timeout_sec=10, update_frequency=1.0, params=None):
        return True

    @mock.patch('bosdyn.client.robot_command.blocking_stand', mocked_blocking_stand)
    @mock.patch('bosdyn.client.robot.Robot.is_powered_on', mocked_is_powered_on)
    @mock.patch('bosdyn.client.power._power_command', mocked_power_command)
    @mock.patch('bosdyn.client.robot.Robot.is_estopped', mocked_is_estopped)
    @mock.patch('bosdyn.client.time_sync.TimeSyncThread.wait_for_sync', mocked_wait_for_sync)
    @mock.patch('bosdyn.client.robot.Robot.sync_with_services_list', mocked_sync_with_services_list)
    @mock.patch('bosdyn.client.common.BaseClient.call', mocked_robot_call)
    def test_hello_spot_function(self):
        """
        Test case for checking the helloSpot.hello_spot function.
        """
        helloSpot.hello_spot(self.robot, self.state_client)
