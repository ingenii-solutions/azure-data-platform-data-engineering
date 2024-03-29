# Ingenii Data Engineering Package

[![Maintainer](https://img.shields.io/badge/maintainer%20-ingenii-orange?style=flat)](https://ingenii.dev/)
[![License](https://img.shields.io/badge/license%20-MPL2.0-orange?style=flat)](https://github.com/ingenii-solutions/azure-data-platform-data-engineering/blob/main/LICENSE)
[![Contributing](https://img.shields.io/badge/howto%20-contribute-blue?style=flat)](https://github.com/ingenii-solutions/data-platform-databricks-runtime/blob/main/CONTRIBUTING.md)

## Details

* Current Version: 0.3.2

## Overview

This package provides utilities for data engineering on Ingenii's Azure Data Platform. This can be both used for local development, and is used in the [Ingenii Databricks Runtime](https://github.com/ingenii-solutions/azure-data-platform-databricks-runtime).

## Usage

Import the package to use the functions within.

```python
import ingenii_data_engineering
```

## dbt

Part of this package validates dbt schemas to ensure they are compatible with Databricks and the larger Ingenii Data Platform. This happens when a data pipeline to ingest a file is run, to make sure a file is ingested correctly.
Full details of how to set up your dbt schema files in your Data Engineering repository can be found in the [Ingenii Data Engineering Example repository](https://github.com/ingenii-solutions/azure-data-platform-data-engineering-example).

## Pre-processing

This package contains code to facilitate the pre-processing of files before they are ingested by the data platform. This allows users to transform any data into a form that is compatible. See details of working with pre-processing functions in the [Ingenii Data Engineering Example repository](https://github.com/ingenii-solutions/azure-data-platform-data-engineering-example).

This package also contains the code to turn the pre-processing scripts into a package, ready to be uploaded and used by the Data Platform. Once this package is installed, the command
```bash
python -m <package name> <command> <folder with pre-processing code>
python -m ingenii_data_engineering pre_processing_package pre_process
```
will generate a `.whl` file in a folder called `dist/`. For more details, see the [Ingenii Data Engineering Example repository](https://github.com/ingenii-solutions/azure-data-platform-data-engineering-example).

## Development

### Prerequisites

1. A working knowledge of [git SCM](https://git-scm.com/downloads)
1. Installation of [Python 3.7.3](https://www.python.org/downloads/)

### Set up

1. Complete the 'Getting Started > Prerequisites' section
1. For Windows only:
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

- `0.3.2`: Further bugfix for JSON UTF-8 BOM
- `0.3.1`: Remove unnecessary functions specific to Databricks
- `0.3.0`: Create pre-processing package using the module
- `0.2.1`: Handle JSON read UTF-8 BOM
- `0.2.0`: Pre-processing happens all in the 'archive' container
- `0.1.5`: Better functionality for column names in .csv files
- `0.1.4`: Handle JSON files
- `0.1.3`: Adding pre-processing utilities
- `0.1.2`: Rearrangement and better split of work with the Databricks Runtime. Better validation
- `0.1.1`: Minor bug fixes
- `0.1.0`: dbt schema validation, pre-processing class
