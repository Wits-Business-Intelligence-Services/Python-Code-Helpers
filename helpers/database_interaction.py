import pandas as __pd__
import helpers
from typing import Optional as __Optional__
import sqlalchemy as __sq__
from logging import Logger as __Logger__
import time as __time__


def current_db_compatible_time() -> str:
    date_created = __time__.strftime("%d/%b/%y %H:%M:%S").upper()
    date_str: str = "to_date('{date_created}','dd/mon/yy hh24:mi:ss')".format(
        date_created=date_created
    )
    return date_str


def check_existence_of_table(
    table_name: str, engine, logger: __Logger__ = None
) -> bool:
    """
    Check existence of table on database.

    :param table_name: (str): Name of table to perform operation on.
    :param engine: (sqlalchemy.engine): DB engine used for DB connection.
    :param logger: (logging.Logger): Logger to use for logging.
    :return: (bool): Existence of table.
    """

    if logger is None:
        logger = helpers.library_backend.MockLogger()

    query: str = helpers.library_backend.generate_check_existence_of_table_query(table_name)
    with helpers.ConnectionManager(engine) as conn:
        try:
            result: __pd__.DataFrame = __pd__.read_sql(query, conn)
            if "1" in result.columns:
                logger.debug(
                    "Table '{table_name}' exists.".format(table_name=table_name)
                )
                return True
        except __sq__.exc.DatabaseError as error:
            if "table or view does not exist" in str(error):
                logger.debug(
                    "Table '{table_name}' does not exist.".format(table_name=table_name)
                )
                return False
            else:
                raise helpers.LoggedDatabaseError(logger, str(error))


def get_db_table_column_names(
    table_name: str, engine, logger: __Logger__ = None
) -> __Optional__[list]:
    """
    Get column names of table on database. Checks for existence of table first.

    :param table_name: (str): Name of table to perform operation on.
    :param engine: (sqlalchemy.engine): DB engine used for DB connection.
    :param logger: (logging.Logger): Logger to use for logging.
    :return: (Optional[list]): List of column names, None if table does not exist.
    """

    if logger is None:
        logger = helpers.library_backend.MockLogger()

    if helpers.check_existence_of_table(table_name, engine):
        query: str = helpers.library_backend.generate_column_names_of_db_table_query(table_name)

        success_msg: str = "Successfully retrieved column names of '{table_name}'.".format(
            table_name=table_name
        )
        error_msg: str = "Failed to retrieve column names of '{table_name}'.".format(
            table_name=table_name
        )

        result: __pd__.DataFrame = helpers.execute_select_query_on_db(
            query, success_msg, error_msg, engine, logger
        )
        col_names: list = list(result.columns)
        logger.debug("Column Names: {column_names}".format(column_names=col_names))
        return col_names
    else:
        return None


def get_db_table_row_count(
    table_name: str, engine, logger: __Logger__ = None
) -> __Optional__[int]:
    """
    Get row count of table on database. Checks for existence of table first.

    :param table_name: (str): Name of table to perform operation on.
    :param engine: (sqlalchemy.engine): DB engine used for DB connection.
    :param logger: (logging.Logger): Logger to use for logging.
    :return: (int): Number of rows, None if table does not exist.
    """

    if logger is None:
        logger = helpers.library_backend.MockLogger()

    query: str = helpers.library_backend.generate_get_number_of_rows_of_db_table_query(table_name)

    success_msg: str = "Successfully retrieved row count for table '{table_name}'.".format(
        table_name=table_name
    )
    error_msg: str = "Failed to retrieve row count for table '{table_name}'.".format(
        table_name=table_name
    )

    try:
        result: __pd__.DataFrame = execute_select_query_on_db(
            query, success_msg, error_msg, engine, logger
        )
        count: int = result["COUNT(*)"].iloc[0]
        return count
    except helpers.LoggedDatabaseError as error:
        if "table or view does not exist" in str(error):
            return None


def truncate_table(table_name: str, engine, logger: __Logger__ = None) -> None:
    """
    Truncate staging or prod table. Checks for existence of table first.

    :param table_name: (str): Name of table to perform operation on.
    :param engine: (sqlalchemy.engine): DB engine used for DB connection.
    :param logger: (logging.logger): Logger to use for logging
    :return: None
    """

    if logger is None:
        logger = helpers.library_backend.MockLogger()

    if helpers.check_existence_of_table(table_name, engine):
        query: str = helpers.library_backend.generate_trunc_db_table_query(table_name)

        success_msg: str = "Successfully truncated table '{table_name}'.".format(
            table_name=table_name
        )
        error_msg: str = "Failed to truncated table '{table_name}'.".format(
            table_name=table_name
        )

        helpers.execute_action_query_on_db(
            query, success_msg, error_msg, engine, logger
        )


def drop_table(table_name: str, engine, logger: __Logger__ = None) -> None:
    """
    Drop table. Checks for existence of table first.

    :param table_name: (str): Name of table to perform operation on.
    :param engine: (sqlalchemy.engine): DB engine used for DB connection.
    :param logger: (logging.logger): Logger to use for logging.
    :return: None
    """

    if logger is None:
        logger = helpers.library_backend.MockLogger()

    if helpers.check_existence_of_table(table_name, engine):
        query: str = helpers.library_backend.generate_drop_db_table_query(table_name)

        success_msg: str = "Successfully dropped '{table_name}'".format(
            table_name=table_name
        )
        error_msg: str = "Failed to drop '{table_name}'".format(table_name=table_name)

        helpers.execute_action_query_on_db(
            query, success_msg, error_msg, engine, logger
        )


def create_table(
    data_results: __pd__.DataFrame,
    table_name: str,
    engine,
    allow_nulls: bool = True,
    logger: __Logger__ = None,
) -> None:
    """

    :param data_results: (pd.DataFrame): Data to use for generating column names and data types.
    :param table_name: (str): Name of table to perform operation on.
    :param engine: (sqlalchemy.engine): DB engine used for DB connection.
    :param allow_nulls: (bool): Allow nulls in table.
    :param logger: (logging.logger): Logger to use for logging.
    :return: None
    """

    if logger is None:
        logger = helpers.library_backend.MockLogger()

    # Check if table already exists and get it's column names.
    db_col_names: __Optional__[list] = get_db_table_column_names(table_name, engine)
    # If the table does not exist
    if not db_col_names:
        # Formulate and execute query to create table on DB
        create_query: str = helpers.library_backend.generate_table_creation_query(
            data_results, table_name, allow_nulls,
        )

        success_msg: str = "Created table '{table_name}'.".format(table_name=table_name)
        error_msg: str = "Failed to create '{table_name}'.".format(
            table_name=table_name
        )

        helpers.execute_action_query_on_db(
            create_query, success_msg, error_msg, engine, logger
        )

    else:
        # Formatting
        db_col_names: list = [x.upper() for x in db_col_names]
        new_data_col_names: list = [
            x.upper().replace(" ", "_") for x in list(data_results.columns)
        ]

        # Convert to sets for comparison operations
        db_col_names_set: set = set(db_col_names)
        new_data_col_names_set: set = set(new_data_col_names)

        # Check for differences
        if db_col_names_set != new_data_col_names_set:
            union: set = db_col_names_set.union(new_data_col_names_set)
            diff: set = (union - new_data_col_names_set).union(union - db_col_names_set)
            raise helpers.LoggedDataError(
                logger,
                "Local data columns do not match DB columns: {diff} for table '{table_name}'".format(
                    diff=diff, table_name=table_name
                ),
            )
        else:
            logger.debug(
                "Column names on DB match those of local data for table '{table_name}'.".format(
                    table_name=table_name
                ),
            )


def upload_data_to_table(
    table_data: __pd__.DataFrame,
    upload_partition_size: int,
    table_name: str,
    engine,
    logger: __Logger__ = None,
) -> None:
    """
    Upload data in table_data DataFrame to table.

    :param table_data: (pandas.DataFrame): data to be uploaded.
    :param upload_partition_size: (int): Number of rows to upload at a time.
    :param table_name: (str): Name of table to perform operation on.
    :param engine: (sqlalchemy.engine) DB engine used for DB connection.
    :param logger: (logging.Logger): Logger to use for logging.
    :return:
    """

    if logger is None:
        logger = helpers.library_backend.MockLogger()

    iterator_index: int = 0
    data_num_records: int = len(table_data.index)

    while (iterator_index + 1) * upload_partition_size < data_num_records:

        query: str = helpers.library_backend.generate_insert_query(
            table_data[
                iterator_index
                * upload_partition_size : (iterator_index + 1)
                * upload_partition_size
            ],
            table_name,
        )
        success_msg: str = "Uploaded rows: {a} - {b} to '{table_name}'".format(
            a=str(iterator_index * upload_partition_size),
            b=str((iterator_index + 1) * upload_partition_size - 1),
            table_name=table_name,
        )

        error_msg: str = "Failed to upload rows: {a} - {b} to '{table_name}'".format(
            a=str(iterator_index * upload_partition_size),
            b=str((iterator_index + 1) * upload_partition_size - 1),
            table_name=table_name,
        )

        helpers.execute_action_query_on_db(
            query, success_msg, error_msg, engine, logger
        )
        iterator_index += 1

    # Final non divisible rows
    query: str = helpers.library_backend.generate_insert_query(
        table_data[iterator_index * upload_partition_size :], table_name,
    )

    success_msg: str = "Uploaded rows: {a} - {b} to '{table_name}'".format(
        a=str(iterator_index * upload_partition_size),
        b=str(data_num_records),
        table_name=table_name,
    )

    error_msg: str = "Failed to upload rows: {a} - {b} to '{table_name}'".format(
        a=str(iterator_index * upload_partition_size),
        b=str(data_num_records),
        table_name=table_name,
    )

    helpers.execute_action_query_on_db(query, success_msg, error_msg, engine, logger)


def update_column_by_value(
    old_value: int,
    new_value: int,
    table_name: str,
    column_name: str,
    engine,
    logger: __Logger__ = None,
) -> None:
    """
    Update all rows in the production DB that have the old value in latest_prediction
    to have the new value.

    :param old_value: (int): Value to select rows by.
    :param new_value: (int): Value to replace old value.
    :param table_name: (str): Name of table to perform operation on.
    :param column_name: (str): Name of column to update.
    :param engine: (sqlalchemy.engine): DB engine used for DB connection.
    :param logger: (logging.logger): Logger to use for logging.
    :return: None
    """

    if logger is None:
        logger = helpers.library_backend.MockLogger()

    query: str = helpers.library_backend.generate_update_column_by_value_query(
        table_name, column_name, old_value, new_value,
    )
    success_msg: str = "Updated rows in '{table_name}' table: '{column_name}'='{old_value}' -> '{column_name}'='{new_value}'.".format(
        table_name=table_name,
        old_value=old_value,
        new_value=new_value,
        column_name=column_name,
    )
    error_msg: str = "Failed to update rows in '{table_name}' table: '{column_name}'='{old_value}' -> '{column_name}'='{new_value}'.".format(
        table_name=table_name,
        old_value=old_value,
        new_value=new_value,
        column_name=column_name,
    )

    helpers.execute_action_query_on_db(query, success_msg, error_msg, engine, logger)


def execute_select_query_on_db(
    query: str, success_msg: str, error_msg: str, engine, logger: __Logger__ = None,
) -> __pd__.DataFrame:
    """
    Execute a returning select query.

    :param query: (str): Query to be executed.
    :param success_msg: (str): Debug message for successful execution.
    :param error_msg: (str): Error message for failed execution.
    :param engine: (sqlalchemy.engine): DB engine used for DB connection.
    :param logger: (logging.Logger): Logger to use for logging.
    :return: (pandas.Dataframe): Date returned from DB.
    """

    if logger is None:
        logger = helpers.library_backend.MockLogger()

    try:
        with helpers.ConnectionManager(engine) as conn:
            result: __pd__.DataFrame = __pd__.read_sql(query, conn)
            logger.debug(success_msg)
    except Exception as e:
        logger.error(error_msg)
        raise helpers.LoggedDatabaseError(logger, str(e))
    return result


def execute_action_query_on_db(
    query: str, success_msg: str, error_msg: str, engine, logger: __Logger__ = None,
) -> None:
    """
    Execute a non-returning, commit required query.

    :param query: (str): Query to be executed.
    :param success_msg: (str): Debug message for successful execution.
    :param error_msg: (str): Error message for failed execution.
    :param engine: (sqlalchemy.engine): DB engine used for DB connection.
    :param logger: (logging.Logger): Logger to use for logging.
    :return: None
    """

    if logger is None:
        logger = helpers.library_backend.MockLogger()

    try:
        with helpers.ConnectionManager(engine) as conn:
            trans = conn.begin()
            conn.execute(query)
            trans.commit()
            logger.debug(success_msg)
    except Exception as e:
        logger.error(error_msg)
        raise helpers.LoggedDatabaseError(logger, str(e))
