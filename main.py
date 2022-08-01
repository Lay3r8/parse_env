import os


class EnvFileFormatError(Exception):
    """
    This error is raised when the .env file is badly formatted (eg. it
    contains something else than comments starting with '#' or KEY=VALUE
    pairs)
    """


def get_env_keypair(line: str) -> tuple:
    """
    Removes a comment from a line containing one or more comments.

    Args:
        line: a line read from a .env file

    Returns:
        The environment keypair

    Raises:
        EnvFileFormatError: environment file format is invalid
    """
    head, _, _ = line.partition('#')
    key_value_string = head.rstrip()
    try:
        key, value = key_value_string.split('=')
    except ValueError:
        raise EnvFileFormatError(f'Invalid .env line: {line}') from ValueError
    return key, value


def read_env_file():
    """
    Reads application constants from a .env file (must be called before
    trying to access os.environ, os.getenv, etc...)
    """
    with open('.env', encoding='utf-8') as f_in:
        lines = f_in.readlines()
        for line in lines:
            if line.startswith('#'):
                continue
            env_key, env_value = get_env_keypair(line)
            os.environ[env_key] = env_value
