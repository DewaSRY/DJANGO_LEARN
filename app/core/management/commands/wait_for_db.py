""" 
Django command ro wait for the database to be available. 
"""

from typing import Any, Optional
import time


from psycopg2 import OperationalError as PSGError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

from django.db import connection


class Command(BaseCommand):
    """Django command to wait for database"""

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        """entry point for command"""

        self.stdout.write("waiting for database ....")
        db_up = False
        while db_up is False:
            try:
                connection.ensure_connection()
                self.check(tags=["default"])
                db_up = True
            except (PSGError, OperationalError) as e:
                self.stdout.write("database unAvailable, waiting 1 second")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("database available "))
