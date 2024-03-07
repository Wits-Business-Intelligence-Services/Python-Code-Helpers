import bis_code_helpers


def set_mock_logging_level(level: bis_code_helpers.LoggingLevels):
    """
    Set the mock logger to a different logging level.

    Supported levels are:
        BISCodeHelpers.LoggingLevels.DEBUG

        BISCodeHelpers.LoggingLevels.INFO

        BISCodeHelpers.LoggingLevels.WARNING

        BISCodeHelpers.LoggingLevels.ERROR

        BISCodeHelpers.LoggingLevels.CRITICAL


    :param level: (BISCodeHelpers.LoggingLevels): Enumeration value for level.
    :return: None
    """
    MockLogger.set_logging_level(level)


class MockLogger:
    """
    A class to mock a logger.
    """

    __logging_level__: int = bis_code_helpers.LoggingLevels.INFO.value

    def __init__(self):
        """
        A class to mock a logger.
        """

    @classmethod
    def set_logging_level(cls, level: bis_code_helpers.LoggingLevels):
        cls.__logging_level__ = level.value

    def debug(self, message: str):
        if MockLogger.__logging_level__ <= bis_code_helpers.LoggingLevels.DEBUG.value:
            print("DEBUG: {message}".format(message=message))
        pass

    def info(self, message: str):
        if MockLogger.__logging_level__ <= bis_code_helpers.LoggingLevels.INFO.value:
            print("INFO: {message}".format(message=message))
        pass

    def warning(self, message: str):
        if MockLogger.__logging_level__ <= bis_code_helpers.LoggingLevels.WARNING.value:
            print("WARNING: {message}".format(message=message))
        pass

    def error(self, message: str):
        if MockLogger.__logging_level__ <= bis_code_helpers.LoggingLevels.ERROR.value:
            print("ERROR: {message}".format(message=message))
        pass

    def critical(self, message: str):
        if MockLogger.__logging_level__ <= bis_code_helpers.LoggingLevels.CRITICAL.value:
            print("CRITICAL: {message}".format(message=message))
        pass
