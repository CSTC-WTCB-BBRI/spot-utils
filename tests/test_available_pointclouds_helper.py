#!/usr/bin/env python
"""Tests for available_pointclouds_helper script"""

# Imports
import mock
import time
import datetime
import subprocess

## Django
from django.test import TestCase

## Local Imports
from api.scripts.available_pointclouds_helper import AvailablePointcloudsHelper

class TestAvailablePointcloudsHelper(TestCase):

  @mock.patch('api.scripts.available_pointclouds_helper.os')
  def test_get_available_pointclouds(self, mock_os):
    mock_os.path.exists.return_value = True
    mock_os.path.isdir.return_value = True
    mock_os.scandir.return_value = [
      type('MockDirEntry', (object,), {'is_dir': lambda: True, 'name': 'spot20230813142200'}),
      type('MockDirEntry', (object,), {'is_dir': lambda: False, 'name': 'not_a_dir_1'}),
      type('MockDirEntry', (object,), {'is_dir': lambda: True, 'name': 'spot20230813142201'}),
      type('MockDirEntry', (object,), {'is_dir': lambda: False, 'name': 'not_a_dir_2'}),
    ]
    
    helper = AvailablePointcloudsHelper()
    result = helper._get_available_pointclouds()

    self.assertEqual(result, ['spot20230813142200', 'spot20230813142201'])

  def test_list(self):
    helper = AvailablePointcloudsHelper()

    helper.pointclouds = ['spot20230813142200', 'spot20230813142201']

    expected_result = [
      {
        'name': 'spot20230813142201',
        'date': '13/08/2023 14:22:01',
        'timestamp': int(time.mktime(datetime.datetime(2023, 8, 13, 14, 22, 1).timetuple()))
      },
      {
        'name': 'spot20230813142200',
        'date': '13/08/2023 14:22:00',
        'timestamp': int(time.mktime(datetime.datetime(2023, 8, 13, 14, 22, 0).timetuple()))
      }
    ]

    result = helper.list()

    self.assertEqual(result, expected_result)
  
  @mock.patch('api.scripts.available_pointclouds_helper.subprocess.run')
  def test_collect_new_pointclouds_success(self, mock_subprocess_run):
    helper = AvailablePointcloudsHelper()

    # Mock subprocess.run to return successfully
    mock_subprocess_run.return_value.returncode = 0

    helper.collect_new_pointclouds()

    mock_subprocess_run.assert_called_once_with(['python', 'manage.py', 'collectstatic', '--noinput'], check=True)

  @mock.patch('api.scripts.available_pointclouds_helper.subprocess.run')
  def test_collect_new_pointclouds_error(self, mock_subprocess_run):
    helper = AvailablePointcloudsHelper()

    mock_subprocess_run.side_effect = subprocess.CalledProcessError(returncode=1, cmd='collectstatic')

    helper.collect_new_pointclouds()

    mock_subprocess_run.assert_called_once_with(['python', 'manage.py', 'collectstatic', '--noinput'], check=True)