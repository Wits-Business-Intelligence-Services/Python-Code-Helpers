import enum as __enum__


class LoggingLevels(__enum__.Enum):
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
