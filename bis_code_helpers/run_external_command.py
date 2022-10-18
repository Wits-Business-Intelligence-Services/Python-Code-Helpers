import subprocess as __subprocess__
import logging as __logging__
from typing import Optional as __Optional__

import bis_code_helpers


def run_external_command(command_arg_list: list, logger: __Optional__[__logging__.Logger] = None) -> str:
    """
    Run an external command, wait for it to finish, check return code, and return
    combined stdout and stderr as as string.

    arg list is in the format ['executable', 'arg0', 'arg1', ...].

    :param command_arg_list: (list): List of args.
    :param logger: (logging.Logger): Logger to use for failure logging.
    :return: (str): Combined stdout and stderr.
    """
    p: __subprocess__.run = __subprocess__.run(
        command_arg_list, stdout=__subprocess__.PIPE, stderr=__subprocess__.STDOUT
    )
    stdout: str = p.stdout.decode()
    # Check that the return code is a success.
    try:
        p.check_returncode()
    except Exception as e:
        if logger:
            raise bis_code_helpers.LoggedSubprocessError(logger, f"{str(e)}\n\nThe output of the subprocess is: {stdout}")
        else:
            print(stdout)
            raise e
    return stdout
