import logging
import os
import os.path
import sys


VERSIONS_DIRECTORY  = '~/.dbt/versions'
GLOBAL_VERSION_FILE = '~/.dbt/version'
LOCAL_VERSION_FILE  = '.dbt_version'

DBT_VERSION_VAR = 'DBT_VERSION'

DBT_PACKAGE_JSON_URL = 'https://pypi.org/pypi/dbt/json'

PYTHON = None
PYTHON_VAR = 'DBTENV_PYTHON'

AUTO_INSTALL: bool = None
AUTO_INSTALL_VAR = 'DBTENV_AUTO_INSTALL'

DEBUG: bool = None
DEBUG_VAR = 'DBTENV_DEBUG'

LOGGER = logging.getLogger('dbtenv')
output_handler = logging.StreamHandler()
output_handler.setFormatter(logging.Formatter('{name} {levelname}:  {message}', style='{'))
output_handler.setLevel(logging.DEBUG)
LOGGER.addHandler(output_handler)
LOGGER.propagate = False
LOGGER.setLevel(logging.INFO)
logger = LOGGER


class DbtenvRuntimeError(RuntimeError):
    pass


def get_versions_directory() -> str:
    return os.path.expanduser(VERSIONS_DIRECTORY)


def get_version_directory(dbt_version: str) -> str:
    return os.path.join(get_versions_directory(), dbt_version)


def get_global_version_file() -> str:
    return os.path.expanduser(GLOBAL_VERSION_FILE)


def get_python() -> str:
    if PYTHON:
        return PYTHON

    if PYTHON_VAR in os.environ:
        return os.environ[PYTHON_VAR]

    # If dbtenv is installed in a virtual environment use the base Python installation's executable.
    base_exec_path = sys.base_exec_prefix
    for possible_python_subpath_parts in [['bin', 'python3'], ['bin', 'python'], ['python.exe']]:
        python_path = os.path.join(base_exec_path, *possible_python_subpath_parts)
        if os.path.isfile(python_path):
            logger.debug(f"Using Python executable `{python_path}`.")
            return python_path

    raise DbtenvRuntimeError(f"No Python executable found in `{base_exec_path}`.")


def set_python(python: str) -> None:
    global PYTHON
    PYTHON = python


def get_auto_install() -> bool:
    if AUTO_INSTALL is not None:
        return AUTO_INSTALL
    if AUTO_INSTALL_VAR in os.environ:
        return string_is_true(os.environ[AUTO_INSTALL_VAR])
    return False


def set_auto_install(auto_install: bool) -> None:
    global AUTO_INSTALL
    AUTO_INSTALL = auto_install


def get_debug() -> bool:
    if DEBUG is not None:
        return DEBUG
    if DEBUG_VAR in os.environ:
        return string_is_true(os.environ[DEBUG_VAR])
    return False


def set_debug(debug: bool) -> None:
    global DEBUG
    DEBUG = debug
    LOGGER.setLevel(logging.DEBUG if debug else logging.INFO)


def string_is_true(string: str) -> bool:
    return isinstance(string, str) and string.strip().lower() in ('1', 't', 'true', 'y', 'yes')


# Enable debug logging during initialization if it's configured.
set_debug(get_debug())
