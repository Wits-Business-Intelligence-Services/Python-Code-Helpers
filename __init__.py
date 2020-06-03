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
    "upload_data_to_table",
    "update_column_by_value",
    "execute_select_query_on_db",
    "execute_action_query_on_db",
    "check_existence_of_table",
    "set_mock_logging_level",
    "LoggingLevels",
    "current_db_compatible_time",
]

from helpers import (
    ConnectionManager,
    create_engine,
    LoggedValueError,
    LoggedDataError,
    LoggedDatabaseError,
    LoggedSubprocessError,
    setup_logging,
    get_db_table_column_names,
    get_db_table_row_count,
    truncate_table,
    drop_table,
    create_table,
    upload_data_to_table,
    update_column_by_value,
    execute_select_query_on_db,
    execute_action_query_on_db,
    check_existence_of_table,
    current_db_compatible_time,
)

from helpers.library_backend import set_mock_logging_level, LoggingLevels
