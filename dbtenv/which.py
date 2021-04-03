import argparse
from typing import List, Optional

import dbtenv
from dbtenv import Args, Dbt, DbtenvError, Environment, Installer, Subcommand, Version
import dbtenv.homebrew
import dbtenv.venv
import dbtenv.version


logger = dbtenv.LOGGER


class WhichSubcommand(Subcommand):
    """
    Show the full path to the executable of the specified dbt version or the dbt version automatically detected from
    the environment.
    """

    name = 'which'

    def add_args_parser(self, subparsers: argparse._SubParsersAction, parent_parsers: List[argparse.ArgumentParser]) -> None:
        parser = subparsers.add_parser(
            self.name,
            parents=parent_parsers,
            description=f"""
                Show the full path to the executable of the specified dbt version or the dbt version automatically
                detected from the environment based on the global `{dbtenv.GLOBAL_VERSION_FILE}` file, local
                `{dbtenv.LOCAL_VERSION_FILE}` files, or {dbtenv.DBT_VERSION_VAR} environment variable.
            """,
            help=self.__doc__
        )
        parser.add_argument(
            'dbt_version',
            nargs='?',
            type=Version,
            metavar='<dbt_version>',
            help="""
                Exact version of dbt to show.
                If not specified, the dbt version will be automatically detected from the environment.
            """
        )

    def execute(self, args: Args) -> None:
        if args.dbt_version:
            version = args.dbt_version
        else:
            version = dbtenv.version.try_get_version(self.env)
            if version:
                logger.info(f"Using dbt {version} (set by {version.source}).")
            else:
                logger.info("No dbt version has been set for the current shell, dbt project, local directory, or globally.")

        if version:
            print(get_dbt(self.env, version).get_executable())


def get_dbt(env: Environment, version: Version) -> Dbt:
    error = DbtenvError(f"No dbt {version} executable found.")

    venv_dbt = None
    if env.use_venv:
        venv_dbt = dbtenv.venv.VenvDbt(env, version)
        try:
            venv_dbt.get_executable()  # Raises an appropriate error if it's not installed.
            if env.primary_installer == Installer.PIP:
                return venv_dbt
        except DbtenvError as venv_error:
            if env.installer == Installer.PIP:
                raise
            else:
                error = venv_error

    if env.use_homebrew:
        homebrew_dbt = dbtenv.homebrew.HomebrewDbt(env, version)
        try:
            homebrew_dbt.get_executable()  # Raises an appropriate error if it's not installed.
            return homebrew_dbt
        except DbtenvError as homebrew_error:
            if env.installer == Installer.HOMEBREW:
                raise
            elif env.primary_installer == Installer.HOMEBREW:
                error = homebrew_error

    if venv_dbt and venv_dbt.is_installed():
        return venv_dbt

    raise error


def try_get_dbt(env: Environment, version: Version) -> Optional[Dbt]:
    try:
        return get_dbt(env, version)
    except Exception as error:
        logger.debug(f"Error getting dbt:  {error}")
        return None
