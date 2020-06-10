Mock Logging
============================================

.. autofunction:: bis_code_helpers.set_mock_logging_level
    :noindex:

``bis_code_helpers`` supports logging in most if not all of it's functions, however there are two modes of logging available:

1. true logging, whereby you pass a ``logging.Logger`` instance to a function, and
2. mock logging, whereby you leave the `logger` argument blank in a function and messages that would usually be logged will be printed.

The mock logger defaults, like a true logger, to INFO level.


True Logging
============================================

.. automodule:: bis_code_helpers
    :noindex:
    :members:
        setup_logging


Connection Management
============================================

.. autofunction:: bis_code_helpers.create_engine
    :noindex:

The ``create_engine`` function is a simple wrapper on top of sqlalchemy's create engine function that handles the Oracle connection string formatting.

.. autoclass:: bis_code_helpers.ConnectionManager
    :noindex:

The ``ConnectionManager`` class is used as such::

    with ConnectionManager(engine) as conn:
        ...

Database Interaction
============================================

.. automodule:: bis_code_helpers
    :noindex:
    :members:
        current_db_compatible_time,
        check_existence_of_table,
        get_db_table_column_names,
        get_db_table_row_count,
        truncate_table,
        create_table,
        drop_table,
        upload_data_to_table,
        update_column_by_value,
        execute_select_query_on_db,
        execute_action_query_on_db

Logged Exceptions
============================================

These are merely exceptions that log their messages.

All of the functions in this package use these over their non-logged counterparts.

.. automodule:: bis_code_helpers
    :noindex:
    :members:
        LoggedValueError,
        LoggedDataError,
        LoggedDatabaseError,
        LoggedSubprocessError