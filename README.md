# Ingenii Data Engineering Package

[![Maintainer](https://img.shields.io/badge/maintainer%20-ingenii-orange?style=flat)](https://ingenii.dev/)
[![License](https://img.shields.io/badge/license%20-MPL2.0-orange?style=flat)](https://github.com/ingenii-solutions/terraform-azurerm-key-vault/blob/main/LICENSE)
[![Contributing](https://img.shields.io/badge/howto%20-contribute-blue?style=flat)](https://github.com/ingenii-solutions/data-platform-databricks-runtime/blob/main/CONTRIBUTING.md)

## Details

* Current Version: 0.1.0

## Overview

This package provides utilities for data engineering on Ingenii's Azure Data Platform. This can be both used for local development, and is used in the [Ingenii Databricks Runtime](https://github.com/ingenii-solutions/azure-data-platform-databricks-runtime).

## Usage

Import the package to use the functions within.

```python
import ingenii_data_engineering
```

## dbt

See details of how we validate dbt schemas in the [dbt README file](DBT.md)

## Pre-processing

See details of working with pre-processing functions in the [pre-processing README file](PREPROCESS.md)

## Development

### Prerequisites

1. A working knowledge of [git SCM](https://git-scm.com/downloads)
1. Installation of [Python 3.7.3](https://www.python.org/downloads/)

### Set up

1. Complete the 'Getting Started > Prerequisites' section
1. For Windows only:
    1. Go to [ezwinports](https://sourceforge.net/projects/ezwinports/files/) - this is required to be able to run `make` commands
    1. Download make-4.2.1-without-guile-w32-bin.zip (get the version without guile)
    1. Extract zip and Copy the contents to C:\ProgramFiles\Git\mingw64\ merging the folders, but do NOT overwrite/replace any exisiting files.
1. Run `make setup`: to copy the .env into place (`.env-dist` > `.env`)

## Getting started

1. Complete the 'Getting Started > Set up' section
1. From the root of the repository, in a terminal (preferably in your IDE) run the following commands to set up a virtual environment:

    ```bash
   python -m venv venv
   . venv/bin/activate
   pip install -r requirements-dev.txt
   pre-commit install
   ```

   or for Windows:
   
    ```bash
   python -m venv venv
   . venv/Scripts/activate
   pip install -r requirements-dev.txt
   pre-commit install
   ```

1. Note: if you get a `permission denied` error when executing the `pre-commit install` command you'll need to run `chmod -R 775 venv/bin/` to recursively update permissions in the `venv/bin/` dir
1. The following checks are run as part of [pre-commit](https://pre-commit.com/) hooks: flake8(note unit tests are not run as a hook)

## Building

1. Complete the 'Getting Started > Set up' section
1. Run `make build` to create the package in `./dist`
1. Run `make clean` to remove dist files

## Testing

1. Complete the 'Getting Started > Set up' and 'Development' sections
1. Run `make test` to run the unit tests using [pytest](https://docs.pytest.org/en/latest/)
1. Run `flake8` to run lint checks using [flake8](https://pypi.org/project/flake8/)
1. Run `make qa` to run the unit tests and linting in a single command
1. Run `make qa` to remove pytest files

## Version History

- `0.1.0`: dbt schema validation, pre-processing class
