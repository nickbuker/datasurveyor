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

<a name="using-surveyor"></a>
## Using Surveyor:

`df`

|    |   id | name    | state   | app_inst   |   lylty |   spend |
|---:|-----:|:--------|:--------|:-----------|--------:|--------:|
|  0 |    1 | Nick    | WA      | True       |       0 |       0 |
|  1 |    2 | Gina    | OR      | True       |       1 |     nan |
|  2 |    3 | Rob     | WA      | False      |       0 |      10 |
|  3 |    4 | Adam    | ID      | True       |       1 |     150 |
|  4 |    5 | Hanna   | WA      | True       |       1 |      12 |
|  5 |    6 | Susan   | Null    | False      |       0 |       0 |
|  6 |    7 | Quentin | WA      | True       |       1 |     nan |
|  7 |    8 | Caitlyn | ID      | True       |       0 |       8 |
|  8 |    9 | Matt    | WA      | True       |       1 |      50 |
|  9 |   10 | Nick    | WA      | True       |       0 |     -10 |



### Binary Features
```python
from surveyor import BinaryFeatures as BF
```

```python
BF.check_all_same(df['app_inst'])
```

|    |   all_same |
|---:|:-----------|
|  0 | False      |


```python
BF.check_all_same(df[['app_inst', 'lylty']])
```

|    | column   | all_same   |
|---:|:---------|:-----------|
|  0 | app_inst | False      |
|  1 | lylty    | False      |


```python
BF.check_mostly_same(df['app_inst'])
```

|    | mostly_same   |   thresh |   mean |
|---:|:--------------|---------:|-------:|
|  0 | False         |     0.95 |    0.8 |

```python
BF.check_mostly_same(df['app_inst'], thresh=0.7)
```

|    | mostly_same   |   thresh |   mean |
|---:|:--------------|---------:|-------:|
|  0 | True          |      0.7 |    0.8 |


```python
BF.check_mostly_same(df[['app_inst', 'lylty']])
```

|    | column   | mostly_same   |   thresh |   mean |
|---:|:---------|:--------------|---------:|-------:|
|  0 | app_inst | False         |     0.95 |    0.8 |
|  1 | lylty    | False         |     0.95 |    0.5 |

```python
BF.check_mostly_same(df[['app_inst', 'lylty']], thresh=0.7)
```

|    | column   | mostly_same   |   thresh |   mean |
|---:|:---------|:--------------|---------:|-------:|
|  0 | app_inst | True          |      0.7 |    0.8 |
|  1 | lylty    | False         |      0.7 |    0.5 |

```python
BF.check_outside_range(df['app_inst'])
```

|    |   outside_range |
|---:|:----------------|
|  0 | False           |


```python
BF.check_outside_range(df[['app_inst', 'lylty']])
```

|    | column   | outside_range   |
|---:|:---------|:----------------|
|  0 | app_inst | False           |
|  1 | lylty    | False           |

### Categorical Features
TODO

### General Features
TODO

### Unique Features
```python
from surveyor import UniqueFeatures as UF
```

```python
UF.check_uniqueness(sample_df['id'])
```

|    | dupes_present   |   dupe_count |   prop_dupe |
|---:|:----------------|-------------:|------------:|
|  0 | False           |            0 |           0 |


```python
UF.check_uniqueness(df[['id', 'name']])
```

|    | column   | dupes_present   |   dupe_count |   prop_dupe |
|---:|:---------|:----------------|-------------:|------------:|
|  0 | id       | False           |            0 |         0   |
|  1 | name     | True            |            1 |         0.1 |



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
