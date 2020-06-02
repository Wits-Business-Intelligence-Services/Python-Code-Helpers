import logging as __logging__


class LoggedValueError(Exception):

    """
    ValueError, but with builtin logging.

    :param logger: (logging.Logger): Logger for logging.
    :param message: (str): Exception message to display.
    """

    def __init__(self, logger: __logging__.Logger, message: str):
        super(LoggedValueError, self).__init__(message)
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

    :param logger: (logging.Logger): Logger for logging.
    :param message: (str): Exception message to display.
    """

    def __init__(self, logger: __logging__.Logger, message: str):
        super(LoggedDataError, self).__init__(message)
        logger.error(message)
        logger.error("----------END:ERROR----------")
        self.message: str = message

    def __str__(self) -> str:
        return "The error in the data is as follows: {error}".format(error=self.message)


class LoggedDatabaseError(Exception):
    """
    DatabaseError, but with builtin logging.

    :param logger: (logging.Logger): Logger for logging.
    :param message: (str): Exception message to display.
    """

    def __init__(self, logger: __logging__.Logger, message: str):
        super(LoggedDatabaseError, self).__init__(message)
        logger.error(message)
        logger.error("----------END:ERROR----------")
        self.message: str = message

    def __str__(self) -> str:
        return "The error in the database is as follows: {error}".format(
            error=self.message
        )


class LoggedSubprocessError(Exception):
    """
    SubprocessError, but with builtin logging.

    :param logger: (logging.Logger): Logger for logging.
    :param message: (str): Exception message to display.
    """

    def __init__(self, logger: __logging__.Logger, message: str):
        super(LoggedSubprocessError, self).__init__(message)
        logger.error(message)
        logger.error("----------END:ERROR----------")
        self.message: str = message

    def __str__(self) -> str:
        return "The error encountered when using subprocess is as follows: {error}".format(
            error=self.message
        )
