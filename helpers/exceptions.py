import logging as __logging__


class LoggedValueError(Exception):
    """
    ValueError, but with builtin logging.
    """

    def __init__(self, logger: __logging__.Logger, message: str):
        logger.error(message)
        logger.error("----------END:ERROR----------")
        self.message: str = message

    def __str__(self) -> str:
        return "The error in the arguments is as follows: {error}".format(
            error=self.message
        )


class LoggedDataError(Exception):
    """
    DataError, but with builtin logging.
    """

    def __init__(self, logger: __logging__.Logger, message: str):
        logger.error(message)
        logger.error("----------END:ERROR----------")
        self.message: str = message

    def __str__(self) -> str:
        return "The error in the data is as follows: {error}".format(error=self.message)


class LoggedDatabaseError(Exception):
    """
    DatabaseError, but with builtin logging.
    """

    def __init__(self, logger: __logging__.Logger, message: str):
        logger.error(message)
        logger.error("----------END:ERROR----------")
        self.message: str = message

    def __str__(self) -> str:
        return "The error in the database is as follows: {error}".format(
            error=self.message
        )
