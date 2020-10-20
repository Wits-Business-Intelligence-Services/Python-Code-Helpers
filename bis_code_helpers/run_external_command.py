import subprocess as __subprocess__


def run_external_command(command_arg_list: list) -> str:
    """
    Run an external command, wait for it to finish, check return code, and return
    combined stdout and stderr as as string.

    arg list is in the format ['executable', 'arg0', 'arg1', ...].

    :param command_arg_list: (list): List of args.
    :return: (str): Combined stdout and stderr.
    """
    p: __subprocess__.run = __subprocess__.run(
        command_arg_list, stdout=__subprocess__.PIPE, stderr=__subprocess__.STDOUT
    )
    # Check that the return code is a success.
    p.check_returncode()

    stdout: str = p.stdout.decode()

    return stdout
