# Surveyor

## Author:
Nick Buker

## Introduction:
Surveyor is a small collection of tools for exploratory data analysis. It leverages Pandas, but the tools are able to ingest either DataFrames or Series. The output is a tidy DataFrame for easy viewing of results. Currently, surveyor focuses on rapidly identifying data quality issues, but the scope will likely expand as the package becomes "battle tested".

## Table of contents:

### Installing surveyor:
- [Surveyor installation instructions](#pip-installing-surveyor)

### Using surveyor:
- [Surveyor use instructions](#using-surveyor)

### Contributing and Testing:
- [Contributing to surveyor](#survey-contribution)
- [Testing surveyor](#surveyor-testing)

<a name="pip-installing-surveyor"></a>
## Installing surveyor:
Surveyor can be install via pip. As always, use of a project-level virtual environment is recommended.

 **Surveyor requires Python >= 3.6.**

```bash
$ pip install surveyor
```

<a name="surveyor-testing"></a>
## Testing:
For those interested in contributing to surveyor forking and editing the project, pytest is the testing framework used. To run the tests, create a virtual environment, install the contents of `dev_requirements.txt`, and run the following command from the root directory of the project. The testing scripts can be found in the `tests/` directory.

```bash
$ pytest
```

To run tests and view coverage, use the below command:

```bash
$ pytest --cov=surveyor
```
