import bis_code_helpers

import logging as __logging__
from os import path as __path__
from os import mkdir as __mkdir__


def setup_logging(
    log_folder: str, unique_log_name: str, logging_level: str
) -> __logging__.Logger:
    """
    Set up a logger with a standardised logging format.

    :param log_folder: (str): Folder to hold log files.
    :param unique_log_name: (str): Log file name.
    :param logging_level: (str): Level for logger.
    :return: (logging.Logger): A fully set up logger.
    """

    # Set logging level
    if logging_level == "DEBUG":
        log_level = __logging__.DEBUG
    elif logging_level == "INFO":
        log_level = __logging__.INFO

    # Create logfile folder
    if not __path__.exists(log_folder):
        __mkdir__(log_folder)

    # Setup logging
    logfile_name: str = unique_log_name + ".log"

    logfile_path: str = __path__.normpath(__path__.join(log_folder, logfile_name))

    __logging__.basicConfig(
        filename=logfile_path,
        level=log_level,
        format="%(asctime)s ||| %(levelname)s ||| %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S %A",
    )

    logger: __logging__.Logger = __logging__.getLogger()
    return logger


def format_text_with_dashes(
        text: str,
        line_width: int,
) -> str:
    """
    Formats a log info entry with dashes and centres the text within.

    Args:
        text (str): text to be formatted and logged
        line_width (int): total line width of dashed log entry

    Returns:
        None

    """
    text_width: int = len(text)
    num_dashes: int = line_width - text_width
    text_even_length: bool = text_width % 2 == 0
    first_dash_substring = '-' * (num_dashes // 2)
    second_dash_substring = first_dash_substring
    if not text_even_length:
        second_dash_substring += '-'

    return first_dash_substring + text + second_dash_substring

