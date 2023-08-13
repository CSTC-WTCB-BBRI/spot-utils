#!/usr/bin/env python
"""Tests for estop_nogui script"""

# Imports
import mock

## Django
from django.test import TestCase

## Local Imports
from api.scripts.estop_nogui import EstopNoGui

class TestEstopNoGui(TestCase):

  @mock.patch('api.scripts.estop_nogui.EstopEndpoint')
  @mock.patch('api.scripts.estop_nogui.EstopKeepAlive')
  def test_estop_no_gui(self, mock_estop_keep_alive, mock_estop_endpoint):
    mock_client = mock.Mock()
    timeout_sec = 10
    estop_name = "TestEstop"

    estop_no_gui = EstopNoGui(mock_client, timeout_sec, estop_name)

    mock_estop_endpoint.assert_called_once_with(mock_client, estop_name, timeout_sec)
    mock_estop_endpoint.return_value.force_simple_setup.assert_called_once()
    mock_estop_keep_alive.assert_called_once_with(mock_estop_endpoint.return_value)

    estop_no_gui.stop()
    mock_estop_keep_alive.return_value.stop.assert_called_once()

    estop_no_gui.allow()
    mock_estop_keep_alive.return_value.allow.assert_called_once()
