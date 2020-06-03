import pandas as __pd__
from typing import Callable as __Callable__
import re as __re__


# ----------------------------------------------------
# Generate query to copy data from staging to production
# ----------------------------------------------------


def generate_table_to_table_insert_query(
    source_table_name: str, target_table_name: str
) -> str:
    """
    Generate query to copy all data from source table to target table.

    :param source_table_name: (str): Source table name.
    :param target_table_name: (str) Target table name.
    :return: (str): Query for copying data.
    """
    query: str = "INSERT INTO {target_table_name} SELECT * FROM {source_table_name}".format(
        source_table_name=source_table_name, target_table_name=target_table_name
    )
    return query


# ----------------------------------------------------
# Generate query to truncate table on database
# ----------------------------------------------------


def generate_trunc_db_table_query(table_name: str) -> str:
    """
    Generate query to truncate table.

    :param table_name: (str): Table to be truncated.
    :return: (str): Query for truncating table.
    """
    query: str = "truncate table {table_name}".format(table_name=table_name)
    return query


# ----------------------------------------------------
# Generate query to drop table on database
# ----------------------------------------------------


def generate_drop_db_table_query(table_name: str) -> str:
    """
    Generate query to drop table.

    :param table_name: (str): Table to be dropped.
    :return: (str): Query for dropping table.
    """
    query: str = "drop table {table_name} purge".format(table_name=table_name)
    return query


# ----------------------------------------------------
# Generate query to get the number of rows of table on database
# ----------------------------------------------------


def generate_get_number_of_rows_of_db_table_query(table_name: str) -> str:
    """
    Generate query to get number of rows in table.

    :param table_name: (str): Table to have it's rows counted.
    :return: (str): Query for getting number of rows of table.
    """
    query: str = "select count(*) from {table_name}".format(table_name=table_name)
    return query


# ----------------------------------------------------
# Generate query to get column names of table on database
# ----------------------------------------------------


def generate_column_names_of_db_table_query(table_name: str):
    """
    Generate query for getting column names of table.

    :param table_name: (str): Table to have it's column names retrieved.
    :return: (str): Query for getting column names of table.
    """
    query: str = "SELECT * FROM {table_name} WHERE rownum < 1".format(
        table_name=table_name
    )
    return query


# ----------------------------------------------------
# Generate query to create table on database
# ----------------------------------------------------


def __generate_table_creation_query__(column_data: str, table_name: str) -> str:
    """
    Generate final query for creating a table from a DataFrame, using data processed in the parent function.

    :param column_data: (str): Data detailing the columns of the new table.
    :param table_name: (str): Name of the new table.
    :return: (str): Query for creating table.
    """
    query: str = """
    CREATE TABLE {table_name}(
        {column_names}
    )
    """.format(
        column_names=column_data, table_name=table_name,
    )
    return query


def generate_table_creation_query(
    data: __pd__.DataFrame, table_name: str, allow_nulls: bool = True,
) -> str:
    """
    Generate query for creating a table based on the data in an inputted DataFrame.
    Performs column name extraction and data type conversion.

    :param data: (DataFrame): Data the table will be based on.
    :param table_name: (str): Name of new table to be created.
    :param allow_nulls: (bool): Allow nulls in table.
    :return: (str): Query for creating table.
    """

    # get data types
    db_table_cols: __pd__.Series = data.dtypes
    # Handle datetime64[ns] objects
    db_table_cols[db_table_cols == "datetime64[ns]"] = "VARCHAR2(200)"

    # convert series data to string so we can replace types
    db_table_cols = db_table_cols.astype("str")

    # replace python / numpy data types with oracle sql data types
    db_table_cols = db_table_cols.str.replace("object", "VARCHAR2(200)")
    db_table_cols = db_table_cols.str.replace("float32", "FLOAT(32)")
    db_table_cols = db_table_cols.str.replace("float64", "FLOAT(64)")
    db_table_cols = db_table_cols.str.replace("int64", "NUMBER")
    db_table_cols = db_table_cols.str.replace("int32", "NUMBER")

    # All columns that are objects and have all values as to_date(...) strings will be dates on the DB
    date_cols: list = [
        x
        for x in data.columns
        if str(data[x].dtype) == "object"
        and len(data[x][data[x].str.contains("to_date")]) == len(data)
    ]
    for col in date_cols:
        db_table_cols[col] = "DATE"

    # convert series to DataFrame
    db_table_cols_frame: __pd__.DataFrame = db_table_cols.to_frame()

    # convert index names to column to replace spaces
    db_table_cols_frame["col_names"] = db_table_cols_frame.index
    db_table_cols_frame.col_names = db_table_cols_frame.col_names.str.replace(" ", "_")
    db_table_cols_frame.columns = ["col_types", "col_names"]
    db_table_cols_frame = db_table_cols_frame[["col_names", "col_types"]]

    # convert DataFrame to list
    db_table_cols_list: list = db_table_cols_frame.to_string(
        header=False, index=False, index_names=False
    ).split("\n")

    # Clean up whitespace
    values = [" ".join(ele.lstrip().split()).lstrip() for ele in db_table_cols_list]

    # Add not null clause to all rows
    if not allow_nulls:
        values = ["{x} NOT NULL".format(x=x) for x in values]

    # convert list to string
    values = ",\n".join(values)

    create_query = __generate_table_creation_query__(
        column_data=values, table_name=table_name
    )
    return create_query


# ----------------------------------------------------
# Generate query to insert data into table
# ----------------------------------------------------


def __generate_insert_query__(
    column_names: str, data_list: list, table_name: str
) -> str:
    """
    Generate final query for inserting a set of rows into a table.

    :param column_names: (str): Names of columns matching new rows.
    :param data_list: (list): List of rows to be inserted.
    :param table_name: (str): Name of table to insert data into.
    :return: (str): Query for inserting set of rows into table.
    """
    query: str = """

    INSERT ALL

    """
    for row in data_list:
        # row = row.replace(",", " ")
        query = (
            query
            + """\nINTO {table_name} ({column_names}) VALUES ({row})""".format(
                table_name=table_name, column_names=column_names, row=row
            )
        )

    query = query + """\nSELECT 1 FROM DUAL"""

    return query


def generate_insert_query(data: __pd__.DataFrame, table_name: str) -> str:
    """
    Generate query for inserting the rows of data into the table.

    :param data: (list): Rows to be inserted into table.
    :param table_name: (str): Name of table to insert rows into.
    :return: (str): Query for inserting rows.
    """
    regex_whitespace_saver: __Callable__ = lambda x: __re__.sub(" ", "___", x)
    regex_whitespace_restorer: __Callable__ = lambda x: __re__.sub("___", " ", x)

    # Copy data so that it can be safely edited
    data = data.copy()

    data_subset: __pd__.DataFrame = data.loc[:, data.dtypes == object]
    data_subset = data_subset.applymap(
        lambda x: "{}{}{}".format("'", x[:100], "'")
        if not isinstance(x, type(None)) and ("to_date" not in x)
        else x
    )

    data.loc[:, data.dtypes == object] = data_subset

    # Handle None values
    data = data.applymap(lambda x: "NULL" if isinstance(x, type(None)) else x)

    insert_data = data.to_string(header=False, index=False, index_names=False).split(
        "\n"
    )

    # Save whitespaces in data
    values: list = [
        __re__.sub(
            r"[a-zA-Z0-9]( |, | & )[a-zA-Z0-9]",
            lambda x: regex_whitespace_saver(x.group()),
            ele,
        )
        for ele in insert_data
    ]

    values = [",".join(ele.split()) for ele in values]
    values = [r.replace("NaN", "'NaN'") for r in values]
    values = [
        __re__.sub(
            r"[a-zA-Z0-9](___|,___|___&___)[a-zA-Z0-9]",
            lambda x: regex_whitespace_restorer(x.group()),
            ele,
        )
        for ele in values
    ]

    col_list = data.columns
    col_list = [col.replace(" ", "_") for col in col_list]
    col_list = ", ".join(col_list)

    insert_query: str = __generate_insert_query__(
        column_names=col_list, data_list=values, table_name=table_name
    )

    return insert_query


# ----------------------------------------------------
# Generate query to update current records in database to new value
# ----------------------------------------------------


def generate_update_column_by_value_query(
    table_name: str, column_name: str, old_value: int, new_value: int
) -> str:
    """
    Generate query to update values of column matching old_value to the value in new_value.

    :param column_name: (str): Name of column to update.
    :param table_name: (str): Name of table to update.
    :param old_value: (int): Value of column to select rows by.
    :param new_value: (str): Value of column that selected rows will be updated to.
    :return: (str): Query to update latest_prediction.
    """
    query: str = """UPDATE {table_name}
    SET 
        {column_name} = {new_value}
    WHERE
        {column_name} = {old_value}""".format(
        table_name=table_name,
        column_name=column_name,
        new_value=new_value,
        old_value=old_value,
    )
    return query


# ----------------------------------------------------
# Generate query to check existence of table on database
# ----------------------------------------------------


def generate_check_existence_of_table_query(table_name: str) -> str:
    """
    Generate query to check existence of table on database.

    :param table_name: (str): Name of table to update.
    :return: (str): Query to check existence of table.
    """
    query: str = "SELECT 1 from {table_name} where rownum < 2".format(
        table_name=table_name
    )
    return query
