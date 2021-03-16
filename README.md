# dbtenv

dbtenv lets you easily install and run multiple versions of [dbt](https://docs.getdbt.com/docs/introduction) using [pip](https://pip.pypa.io/) with [Python virtual environments](https://docs.python.org/3/library/venv.html), or optionally using [Homebrew](https://brew.sh/) on Mac or Linux.

### Table of contents
- **[Installation](#installation)**
- **[How it works](#how-it-works)**
  - [Using pip and/or Homebrew](#using-pip-andor-homebrew)
  - [Installing dbt versions](#installing-dbt-versions)
  - [Switching between dbt versions](#switching-between-dbt-versions)
  - [Running dbt versions](#running-dbt-versions)
  - [Running dbt with dbtenv more seamlessly](#running-dbt-with-dbtenv-more-seamlessly)
  - [Uninstalling dbt versions](#uninstalling-dbt-versions)
- **[Development](#development)**
  - [Development setup](#development-setup)


## Installation

Run `pip3 install git+https://github.com/brooklyn-data/dbtenv#egg=dbtenv`.


## How it works

Run `dbtenv --help` to see some overall documentation for dbtenv, including its available sub-commands, and run `dbtenv <sub-command> --help` to see documentation for that sub-command.

### Using pip and/or Homebrew
By default dbtenv uses [pip](https://pip.pypa.io/) to install dbt versions from the [Python Package Index](https://pypi.org/project/dbt/#history) into Python virtual environments within `~/.dbt/versions`.

However, on Mac or Linux systems dbtenv will automatically detect and use any version-specific dbt installations from [Homebrew](https://brew.sh/) (e.g. `dbt@0.19.0` but not plain `dbt`), and you can have dbtenv use Homebrew to install new dbt versions by setting a `DBTENV_DEFAULT_INSTALLER=homebrew` environment variable, or specifying `--installer homebrew` when running `dbtenv install`.

### Installing dbt versions
You can run `dbtenv versions` to list the versions of dbt available to install, and run `dbtenv install <version>` to install a version.

If you don't want to have to run `dbtenv install <version>` manually, you can set a `DBTENV_AUTO_INSTALL=true` environment variable so that as you run commands like `dbtenv version` or `dbtenv execute` any dbt version specified that isn't already installed will be installed automatically.

Some tips when dbtenv is using pip:
- You can have dbtenv only install Python packages that were actually available on the date the dbt version was released by setting a `DBTENV_SIMULATE_RELEASE_DATE=true` environment variable, or specifying `--simulate-release-date` when running `dbtenv install`.
  This can help if newer versions of dbt's dependencies are causing installation problems.
- By default dbtenv uses whichever Python version it was installed with to install dbt, but that can be changed by setting a `DBTENV_PYTHON` environment variable to the path of a different Python executable, or specifying `--python <path>` when running `dbtenv install`.
  - **dbt currently isn't compatible with Python 3.9 or above**, so if dbtenv was installed with Python 3.9 or above you will need to specify a compatible Python version to install dbt.

### Switching between dbt versions
dbtenv determines which dbt version to use by trying to read it from the following sources, in this order, using the first one it finds:

1. The `dbtenv execute` command's optional `--dbt <version>` argument.
2. The `DBT_VERSION` environment variable.
3. The first `.dbt_version` file found by searching in the current directory and then in each successive parent directory.
4. The `~/.dbt/version` file.

You can:
- Run `dbtenv version --global <version>` to set the dbt version globally in the `~/.dbt/version` file.
- Run `dbtenv version --local <version>` to set the dbt version for the current directory in a `.dbt_version` file.
- Run `dbtenv version` to show which dbt version dbtenv determines dynamically based on the current environment.
- Run `dbtenv which` to show the full path to the executable of the dbt version dbtenv determines dynamically based on the current environment.

### Running dbt versions
Run `dbtenv execute -- <dbt arguments>` to execute the dbt version determined dynamically based on the current environment, or run `dbtenv execute --dbt <version> -- <dbt arguments>` to execute the specified dbt version.

For example:
- `dbtenv execute -- run` will execute `dbt run` using the version determined dynamically based on the current environment.
- `dbtenv execute --dbt 0.19.0 -- run` will execute `dbt run` using dbt 0.19.0.

**Important:**  It's highly recommended to put two dashes with spaces on both sides before the list of dbt arguments (as shown in the examples above) so that dbtenv doesn't try to interpret the dbt arguments itself.

### Running dbt with dbtenv more seamlessly
For a more seamless experience you can define a `dbt` alias or function in your shell to run `dbtenv execute -- <dbt arguments>` and dynamically determine which dbt version to use whenever you type dbt commands like `dbt run` or `dbt test`.

Some examples:
- In **bash** you could add the following alias in your `~/.bash_profile` file:
  ```bash
  alias dbt='dbtenv execute --'
  ```
- In **Windows PowerShell** aliases can't include additional arguments, but you could add the following function in your `~\Documents\PowerShell\Microsoft.PowerShell_profile.ps1` file:
  ```PowerShell
  function dbt { dbtenv execute -- @Args }
  ```

Note that after adding such a `dbt` alias/function to your shell profile you'll need to reload the profile to activate it (e.g. by running `. ~/.bash_profile` in bash, or `. $PROFILE` in PowerShell).

### Uninstalling dbt versions
You can run `dbtenv versions --installed` to list the versions of dbt that dbtenv has installed under `~/.dbt/versions` and/or with Homebrew, and then run `dbtenv uninstall <version>` to uninstall a version.


## Development

### Development setup
1. Clone this repository onto your computer.
2. If you want to isolate the dbtenv development setup (e.g. because you have dbtenv installed normally), create and activate a [Python virtual environment](https://docs.python.org/3/library/venv.html).
3. Run `pip3 install --editable <path to cloned repo>`.
