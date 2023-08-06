"""
Support for using PostgreSQL as a source of data.
"""

from sinai.adaptors.postgresql import Postgresql
from sinai.sources.base import Source


class PostgresSource(Postgresql, Source):
    """Gets data from PostgreSQL databases."""

    ...
