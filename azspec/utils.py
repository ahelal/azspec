''' Common utils '''

import subprocess
from os import getenv
from knack.util import CLIError


def run_command(bin_path, args=None, interactive=False, cwd=None, allow_non_zero_return=False):
    """
    Run CLI commands
    Returns: stdout, stderr  strings
    Exceptions: raise CLIError on execution error
    """

    process = None
    stdout = None
    stderr = None
    try:
        cmd_args = [rf"{bin_path}"]
        if args:
            cmd_args = cmd_args + args
        # _LOGGER.debug(" Running a command %s", cmd_args)
        if interactive:
            subprocess.check_call(cmd_args, cwd=cwd)
            return "", "", 0
        process = subprocess.run(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, check=False)
        stdout = process.stdout.decode('utf-8')
        stderr = process.stderr.decode('utf-8')
        if not allow_non_zero_return:
            process.check_returncode()
        return stdout, stderr, process.returncode
    except subprocess.CalledProcessError as error:
        context = f"Run command error. {str(error)}"
        if stdout:
            context = f"{context} stdout:{stdout}"
        if stderr:
            context = f"{context} stdout:{stderr}"
        raise CLIError(context) from error


def convert_to_list_if_need(param):
    ''' Checks if parameter is a list if not return singe element list '''
    if isinstance(param, list):
        return param
    if param is None or param == "":
        return []
    return [param]


def get_value(env_name, key_name, kwargs, default=None):
    ''' Get value from os env then from kwargs if not fall back to default'''
    if getenv(env_name, None):
        return getenv(env_name)
    if kwargs.get(key_name, None):
        return kwargs.get(key_name)
    return default
