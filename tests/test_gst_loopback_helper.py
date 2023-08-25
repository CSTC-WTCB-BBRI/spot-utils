#!/usr/bin/env python
"""Tests for gst_loopback_helper script"""

# Imports
import mock
import os

## Django
from django.test import TestCase

## Local Imports
from api.scripts.gst_loopback_helper import GstLoopbackHelper

## Environment variables
from dotenv import load_dotenv
from manage import ROOT_DIR

load_dotenv(ROOT_DIR + '.env')
ROBOT_LIBUVC_THETA_SAMPLE_ROOT_DIR = os.getenv('ROBOT_LIBUVC_THETA_SAMPLE_ROOT_DIR')

class TestGstLoopbackHelper(TestCase):

  @mock.patch('api.scripts.gst_loopback_helper.subprocess.Popen')
  def test_start_gst_loopback(self, mock_subprocess_popen):
    mock_ssh_proc = mock.Mock()
    mock_subprocess_popen.return_value = mock_ssh_proc

    helper = GstLoopbackHelper()
    helper.start()

    expected_cmd = ROBOT_LIBUVC_THETA_SAMPLE_ROOT_DIR + "/gst/gst_loopback\n"
    mock_ssh_proc.stdin.write.assert_called_once_with(expected_cmd)

  @mock.patch('api.scripts.gst_loopback_helper.subprocess.Popen')
  def test_stop_gst_loopback(self, mock_subprocess_popen):
    mock_ssh_proc = mock.Mock()
    mock_subprocess_popen.return_value = mock_ssh_proc

    helper = GstLoopbackHelper()
    helper.stop()

    expected_cmds = ["\n", "exit\n"]
    mock_ssh_proc.stdin.write.assert_has_calls([mock.call(cmd) for cmd in expected_cmds])

    mock_ssh_proc.stdin.close.assert_called_once()
