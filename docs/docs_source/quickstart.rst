Introduction
============================================

The bis_code_helpers package is a set of ease-of-use functions that allows one to build standardised Python software at Wits BIS.


Installation
============================================

To install this package, run the following within the directory containing `setup.py`::

    pip install .

This will install ensure the package's dependencies are installed and then install the package in the currently active python environment.


Usage
============================================

The package includes a bunch of functions that may be useful and don't necessarily follow one theme.

A major component of this package is database interaction. All functions that interact with a database take a SQLAlchemy `engine` argument, creates a temporary connection for that interaction using the engine, performs the interaction and then closes the connection.

Here is an example:

1. Import the package::

    import bis_code_helpers

2. Create an engine::

    USER: str = "Kyle"
    PASS: str = "1234"
    DB: str = "bi.example.org:1234/SERVICE"

    engine = bis_code_helpers.create_engine(USER, PASS, DB)

3. Get the list of column names from a table on the DB linked to the engine::

    TABLE_NAME: str = "TEST_TABLE"

    column_names: list = bis_code_helpers.get_db_table_column_names(TABLE_NAME, engine)

