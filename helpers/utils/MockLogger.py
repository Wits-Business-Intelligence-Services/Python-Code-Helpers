import helpers
import enum


class LoggingLevels(enum.Enum):
    """
    Enumeration of mock logger logging levels.

    Supported levels are:
        DEBUG

        INFO

        WARNING

        ERROR

        CRITICAL
    """

    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4


def set_mock_logging_level(level: LoggingLevels):
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

    __logging_level__: int = LoggingLevels.INFO.value

    def __init__(self):
        """
        A class to mock a logger.
        """

    @classmethod
    def set_logging_level(cls, level: LoggingLevels):
        cls.__logging_level__ = level.value

    def debug(self, message: str):
        if MockLogger.__logging_level__ <= LoggingLevels.DEBUG.value:
            print("DEBUG: {message}".format(message=message))
        pass

    def info(self, message: str):
        if MockLogger.__logging_level__ <= LoggingLevels.INFO.value:
            print("INFO: {message}".format(message=message))
        pass

    def warning(self, message: str):
        if MockLogger.__logging_level__ <= LoggingLevels.WARNING.value:
            print("WARNING: {message}".format(message=message))
        pass

    def error(self, message: str):
        if MockLogger.__logging_level__ <= LoggingLevels.ERROR.value:
            print("ERROR: {message}".format(message=message))
        pass

    def critical(self, message: str):
        if MockLogger.__logging_level__ <= LoggingLevels.CRITICAL.value:
            print("CRITICAL: {message}".format(message=message))
        pass
