"""
Support for using PostgreSQL as a source or store for data.
"""

try:
    import psycopg2
except ImportError:
    HAS_POSTGRES = False
else:
    HAS_POSTGRES = True


from sinai.exceptions import DependencyMissing
from sinai.types import MonitorInstance


class Postgresql:
    """Connects to from PostgreSQL databases."""

    connection_string = "dbname=test user=postgres"

    def __init__(self, monitor: MonitorInstance):
        self.monitor = monitor
        if not HAS_POSTGRES:
            raise DependencyMissing(
                "psycopg2 library required for using PostgreSQL databases."
            )
        self.conn = psycopg2.connect(self.connection_string)

    def __del__(self):
        self.conn.close()
