#!/usr/bin/env python
"""Tests for spot_slam script"""

# Imports
import mock
import json

## Django
from django.test import TestCase

# Local Imports
from api.scripts.spot_slam_helper import SpotSLAMHelper

class TestSpotSLAMHelper(TestCase):

  @mock.patch('api.scripts.spot_slam_helper.requests.get')
  def test_launch(self, mock_requests_get):
    expected_message = "Spot-SLAM launched successfully"
    expected_response = {"msg": expected_message}
    mock_requests_get.return_value.content = json.dumps(expected_response).encode()

    helper = SpotSLAMHelper()
    response = helper.launch()

    self.assertEqual(response, json.dumps(expected_message, indent=2))

  @mock.patch('api.scripts.spot_slam_helper.requests.get')
  def test_authorize(self, mock_requests_get):
    expected_message = "Spot-SLAM authorized"
    expected_response = {"msg": expected_message}
    mock_requests_get.return_value.content = json.dumps(expected_response).encode()

    helper = SpotSLAMHelper()
    response = helper.authorize()

    self.assertEqual(response, json.dumps(expected_message, indent=2))

  @mock.patch('api.scripts.spot_slam_helper.requests.get')
  def test_start(self, mock_requests_get):
    expected_message = "Spot-SLAM started capturing LiDAR data"
    expected_response = {"msg": expected_message}
    mock_requests_get.return_value.content = json.dumps(expected_response).encode()

    helper = SpotSLAMHelper()
    response = helper.start()

    self.assertEqual(response, json.dumps(expected_message, indent=2))

  @mock.patch('api.scripts.spot_slam_helper.requests.get')
  def test_stop(self, mock_requests_get):
    expected_message = "Spot-SLAM stopped capturing LiDAR data"
    expected_response = {"msg": expected_message}
    mock_requests_get.return_value.content = json.dumps(expected_response).encode()

    helper = SpotSLAMHelper()
    response = helper.stop()

    self.assertEqual(response, json.dumps(expected_message, indent=2))

  @mock.patch('api.scripts.spot_slam_helper.requests.get')
  def test_save(self, mock_requests_get):
    expected_message = "LiDAR data saved in PCD format"
    expected_response = {"msg": expected_message}
    mock_requests_get.return_value.content = json.dumps(expected_response).encode()

    helper = SpotSLAMHelper()
    response = helper.save()

    self.assertEqual(response, json.dumps(expected_message, indent=2))

  @mock.patch('api.scripts.spot_slam_helper.requests.get')
  def test_potree(self, mock_requests_get):
    expected_message = "LiDAR data exported to Potree format"
    expected_response = {"msg": expected_message}
    mock_requests_get.return_value.content = json.dumps(expected_response).encode()

    helper = SpotSLAMHelper()
    response = helper.potree()

    self.assertEqual(response, json.dumps(expected_message, indent=2))
