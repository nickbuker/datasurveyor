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

# TODO: not yet deployed to PyPI
```bash
$ pip install surveyor
```

<a name="using-surveyor"></a>
## Using Surveyor:

To demonstrate the tools available in surveyor, let's use a Pandas DataFrame named `df`.

|    |   id | name    | state   | app_inst   |   lylty |   spend |
|---:|-----:|:--------|:--------|:-----------|--------:|--------:|
|  0 |    1 | Nick    | WA      | True       |       0 |       0 |
|  1 |    2 | Gina    | OR      | True       |       1 |     nan |
|  2 |    3 | Rob     | WA      | False      |       0 |      10 |
|  3 |    4 | Adam    | ID      | True       |       1 |     150 |
|  4 |    5 | Hanna   | WA      | True       |       1 |      12 |
|  5 |    6 | Susan   | Null    | False      |       0 |       0 |
|  6 |    7 | Quentin | WA      | True       |       1 |     nan |
|  7 |    8 | Caitlyn | unknown | True       |       0 |       8 |
|  8 |    9 | Matt    | WA      | True       |       1 |      50 |
|  9 |   10 | Nick    | WA      | True       |       0 |     -10 |

A data dictionary for `df` is below.

| column   | dtype   | description                |
|:---------|:--------|:---------------------------|
| id       | int64   | unique customer identifier |
| name     | object  | customer name              |
| state    | object  | state of residence         |
| platform | object  | system platform            |
| app_inst | bool    | app installation flag      |
| lylty    | int64   | loyalty program flag       |
| spend    | float64 | total customer spend       |

### Binary features

#### Description
Surveyor expects binary features to have two possible values and to be stored as bools or integers (with values of 0 or 1). In the example data, `app_inst` and `lylty` are binary features.

#### Importing BinaryFeatures
The binary feature tools from surveyor can be imported with the command below.

```python
from surveyor import BinaryFeatures as BF
```

#### Checking of all values the same


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
```python
from surveyor import CategoricalFeatures as CF
```

```python
CF.check_mostly_same(df['state'])
```

|    | mostly_same   |   thresh | most_common   |   count |   prop |
|---:|:--------------|---------:|:--------------|--------:|-------:|
|  0 | False         |     0.95 | WA            |       6 |    0.6 |

```python
CF.check_mostly_same(df['state'], thresh=0.6)
```

|    | mostly_same   |   thresh | most_common   |   count |   prop |
|---:|:--------------|---------:|:--------------|--------:|-------:|
|  0 | True          |      0.6 | WA            |       6 |    0.6 |

```python
CF.check_mostly_same(df[['state', 'platform']])
```

|    | column   | mostly_same   |   thresh | most_common   |   count |   prop |
|---:|:---------|:--------------|---------:|:--------------|--------:|-------:|
|  0 | state    | False         |     0.95 | WA            |       6 |    0.6 |
|  1 | platform | False         |     0.95 | ios           |       5 |    0.5 |

```python
CF.check_mostly_same(df[['state', 'platform']], thresh=0.6)
```

|    | column   | mostly_same   |   thresh | most_common   |   count |   prop |
|---:|:---------|:--------------|---------:|:--------------|--------:|-------:|
|  0 | state    | True          |      0.6 | WA            |       6 |    0.6 |
|  1 | platform | False         |      0.6 | ios           |       5 |    0.5 |

```python
CF.check_n_categories(df['state'])
```

|    |   n_categories |
|---:|---------------:|
|  0 |              4 |

```python
CF.check_n_categories(df[['state', 'platform']])
```

|    | column   |   n_categories |
|---:|:---------|---------------:|
|  0 | state    |              4 |
|  1 | platform |              3 |

### General Features
```python
from surveyor import GeneralFeatures as GF
```

```python
GF.check_fuzzy_nulls(df['state'])
```

|    | fuzzy_nulls_present   |   fuzzy_null_count |   prop_fuzzy_null |
|---:|:----------------------|-------------------:|------------------:|
|  0 | True                  |                  1 |               0.1 |

```python
GF.check_fuzzy_nulls(df['state'], add_fuzzy_nulls=['unknown'])
```
|    | fuzzy_nulls_present   |   fuzzy_null_count |   prop_fuzzy_null |
|---:|:----------------------|-------------------:|------------------:|
|  0 | True                  |                  2 |               0.2 |

```python
GF.check_fuzzy_nulls(df)
```

|    | column   | fuzzy_nulls_present   |   fuzzy_null_count |   prop_fuzzy_null |
|---:|:---------|:----------------------|-------------------:|------------------:|
|  0 | id       | False                 |                  0 |               0   |
|  1 | name     | False                 |                  0 |               0   |
|  2 | state    | True                  |                  1 |               0.1 |
|  3 | platform | False                 |                  0 |               0   |
|  4 | app_inst | False                 |                  0 |               0   |
|  5 | lylty    | False                 |                  0 |               0   |
|  6 | spend    | False                 |                  0 |               0   |

```python
GF.check_fuzzy_nulls(df, add_fuzzy_nulls=['unknown'])
```

|    | column   | fuzzy_nulls_present   |   fuzzy_null_count |   prop_fuzzy_null |
|---:|:---------|:----------------------|-------------------:|------------------:|
|  0 | id       | False                 |                  0 |               0   |
|  1 | name     | False                 |                  0 |               0   |
|  2 | state    | True                  |                  2 |               0.2 |
|  3 | platform | False                 |                  0 |               0   |
|  4 | app_inst | False                 |                  0 |               0   |
|  5 | lylty    | False                 |                  0 |               0   |
|  6 | spend    | False                 |                  0 |               0   |

```python
GF.check_nulls(df['spend'])
```

|    | nulls_present   |   null_count |   prop_null |
|---:|:----------------|-------------:|------------:|
|  0 | True            |            2 |         0.2 |

```python
GF.check_nulls(df)
```

|    | column   | nulls_present   |   null_count |   prop_null |
|---:|:---------|:----------------|-------------:|------------:|
|  0 | id       | False           |            0 |         0   |
|  1 | name     | False           |            0 |         0   |
|  2 | state    | False           |            0 |         0   |
|  3 | platform | False           |            0 |         0   |
|  4 | app_inst | False           |            0 |         0   |
|  5 | lylty    | False           |            0 |         0   |
|  6 | spend    | True            |            2 |         0.2 |

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
