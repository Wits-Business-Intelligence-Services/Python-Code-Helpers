import sys
import os

# Allow package relative imports and referencing
package_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([package_directory])

# Select only those objects that you want imported
__all__ = [
    "ConnectionManager",
    "create_engine",
    "LoggedValueError",
    "LoggedDataError",
    "LoggedDatabaseError",
    "LoggedSubprocessError",
    "setup_logging",
    "get_db_table_column_names",
    "get_db_table_row_count",
    "truncate_table",
    "drop_table",
    "create_table",
    "upload_data_to_table"
]

from .helpers import *

# from .helpers.connection_management import (
#     ConnectionManager,
#     create_engine,
# )
# from .helpers.logged_exceptions import (
#     LoggedValueError,
#     LoggedDataError,
#     LoggedDatabaseError,
#     LoggedSubprocessError,
# )
# from .helpers.logging_helpers import setup_logging
