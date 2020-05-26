import logging as __logging__
from os import path as __path__
from os import mkdir as __mkdir__


def setup_logging(log_folder: str, unique_log_name: str, logging_level: str) -> __logging__.Logger:

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




