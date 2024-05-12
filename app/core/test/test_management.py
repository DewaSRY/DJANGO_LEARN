""" 
Test custom django management command
"""

import time
from unittest.mock import patch
from psycopg2 import OperationalError as PSGError

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch("core.management.commands.wait_for_db.Command.check")
class TestManagement(SimpleTestCase):
    """Test command"""

    def test_wait_for_simple_commend(self, patched_check: BaseCommand.check):
        """test for database if database ready"""
        patched_check.return_value = True
        call_command("wait_for_db")
        patched_check.assert_called_once_with(tags=["default"])

    @patch("time.sleep")
    def test_wait_for_db_delay(
        self, patched_sleep: time.sleep, patched_check: BaseCommand.check
    ):
        """test waiting for database when getting OperationalError"""
        patched_check.side_effect = [PSGError] * 2 + [OperationalError] * 3 + [True]
        call_command("wait_for_db")
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(tags=["default"])
