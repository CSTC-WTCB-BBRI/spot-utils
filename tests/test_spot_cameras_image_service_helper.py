#!/usr/bin/env python
"""Tests for spot_cameras_image_service_helper script"""

# Imports
import mock
import os

## Django
from django.test import TestCase

## Local Imports
from api.scripts.spot_cameras_image_service_helper import SpotCamerasImageServiceHelper

## Environment variables
from dotenv import load_dotenv
from manage import ROOT_DIR

load_dotenv(ROOT_DIR + '.env')
ROBOT_SPOT_UTILS_ROOT_DIR = os.getenv('ROBOT_SPOT_UTILS_ROOT_DIR')

class TestSpotCamerasImageServiceHelper(TestCase):

  @mock.patch('api.scripts.spot_cameras_image_service_helper.subprocess.Popen')
  def test_start_spot_cameras_image_service(self, mock_subprocess_popen):
    mock_ssh_proc = mock.Mock()
    mock_subprocess_popen.return_value = mock_ssh_proc

    helper = SpotCamerasImageServiceHelper()
    helper.start()

    expected_cmds = [
      "cd " + ROBOT_SPOT_UTILS_ROOT_DIR + "/spot-services/SpotCameras\n",
      "docker-compose up -d\n"
    ]
    mock_ssh_proc.stdin.write.assert_has_calls([mock.call(cmd) for cmd in expected_cmds])

  @mock.patch('api.scripts.spot_cameras_image_service_helper.subprocess.Popen')
  def test_stop_spot_cameras_image_service(self, mock_subprocess_popen):
    mock_ssh_proc = mock.Mock()
    mock_subprocess_popen.return_value = mock_ssh_proc

    helper = SpotCamerasImageServiceHelper()
    helper.stop()

    expected_cmds = [
      "cd " + ROBOT_SPOT_UTILS_ROOT_DIR + "/spot-services/SpotCameras\n",
      "docker-compose down\n"
    ]
    mock_ssh_proc.stdin.write.assert_has_calls([mock.call(cmd) for cmd in expected_cmds])

    mock_ssh_proc.stdin.close.assert_called_once()
