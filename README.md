# Datasurveyor

## Author:
Nick Buker

## Introduction:
Datasurveyor is a small collection of tools for exploratory data analysis. It leverages Pandas, but the tools are able to ingest either DataFrames or Series. The output is a tidy DataFrame for easy viewing of results. Currently, datasurveyor focuses on rapidly identifying data quality issues, but the scope will likely expand as the package becomes "battle tested".

## Table of contents:

### Installing datasurveyor:
[Datasurveyor installation instructions](#pip-installing-datasurveyor)

### Using datasurveyor:
[Datasurveyor use instructions](#using-datasurveyor)
- [Binary features](#binary-features)
    - [Importing BinaryFeatures](#binary-features-import)
    - [Checking if all values the same](#binary-features-all-same)
    - [Checking if values are mostly the same](#binary-features-mostly-same)
    - [Checking the range](#binary-features-range)
- [Categorical features](#categorical-features)
    - [Importing CategoricalFeatures](#categorical-features-import)
    - [Checking if values are mostly the same](#categorical-features-import)
    - [Checking number of categories](#categorical-features-n-categories)
- [General features](#general-features)
    - [Importing GeneralFeatures](#general-features-import)
    - [Checking for nulls](#general-features-nulls)
    - [Checking for fuzzy nulls](#general-features-fuzzy-nulls)
- [Unique features](#unique-features)
    - [Importing UniqueFeatures](#unique-features-import)
    - [Checking uniqueness](#unique-features-uniqueness)

### Contributing and Testing:
- [Contributing to datasurveyor](#survey-contrib)
- [Testing datasurveyor](#datasurveyor-test)


<a name="pip-installing-datasurveyor"></a>

## Installing datasurveyor:
Datasurveyor can be install via pip. As always, use of a project-level virtual environment is recommended. **Note: Datasurveyor requires Python >= 3.6.**

```bash
$ pip install datasurveyor
```


<a name="using-datasurveyor"></a>

## Using Datasurveyor

To demonstrate the tools available in datasurveyor, let's use a Pandas DataFrame named `df`.

|    |   id | name    | state   | platform   | app_inst   |   lylty |   spend |
|---:|-----:|:--------|:--------|:-----------|:-----------|--------:|--------:|
|  0 |    1 | Nick    | WA      | ios        | True       |       0 |       0 |
|  1 |    2 | Gina    | OR      | android    | True       |       1 |     nan |
|  2 |    3 | Rob     | WA      | ios        | False      |       0 |      10 |
|  3 |    4 | Adam    | ID      | web        | True       |       1 |     150 |
|  4 |    5 | Hanna   | WA      | ios        | True       |       1 |      12 |
|  5 |    6 | Susan   | Null    | android    | False      |       0 |       0 |
|  6 |    7 | Quentin | WA      | ios        | True       |       1 |     nan |
|  7 |    8 | Caitlyn | unknown | web        | True       |       0 |       8 |
|  8 |    9 | Matt    | WA      | web        | True       |       1 |      50 |
|  9 |   10 | Nick    | WA      | ios        | True       |       0 |     -10 |


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


<a name="binary-features"></a>

## Binary features

### Description
The methods within `BinaryFeatures` are intended for use with binary data (data with two possible values). Datasurveyor expects binary features to be stored as bools or integers (with values of 0 or 1). In the example data, `app_inst` and `lylty` are binary features.


<a name="binary-features-import"></a>

### Importing BinaryFeatures
The binary feature tools can be imported with the command below.

```python
from datasurveyor import BinaryFeatures as BF
```


<a name="binary-features-all-same"></a>

### Checking if all values the same
The `check_all_same` method can be used to check if binary features contain exclusively the same value. This method can be applied to a single binary feature or a collection of binary features.

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


<a name="binary-features-mostly-same"></a>

### Checking if values are mostly the same
The `check_mostly_same` method can be used to check if binary features contain mostly the same value (default threshold 95%). This method can be applied to a single binary feature or a collection of binary features.

```python
BF.check_mostly_same(df['app_inst'])
```

|    | mostly_same   |   thresh |   mean |
|---:|:--------------|---------:|-------:|
|  0 | False         |     0.95 |    0.8 |

```python
BF.check_mostly_same(df[['app_inst', 'lylty']])
```

|    | column   | mostly_same   |   thresh |   mean |
|---:|:---------|:--------------|---------:|-------:|
|  0 | app_inst | False         |     0.95 |    0.8 |
|  1 | lylty    | False         |     0.95 |    0.5 |

The user can specify whatever threshold is appropriate for their usecase. If `thresh=0.7` is applied, the method will flag features with at least 70% the same value.

```python
BF.check_mostly_same(df['app_inst'], thresh=0.7)
```

|    | mostly_same   |   thresh |   mean |
|---:|:--------------|---------:|-------:|
|  0 | True          |      0.7 |    0.8 |

```python
BF.check_mostly_same(df[['app_inst', 'lylty']], thresh=0.7)
```

|    | column   | mostly_same   |   thresh |   mean |
|---:|:---------|:--------------|---------:|-------:|
|  0 | app_inst | True          |      0.7 |    0.8 |
|  1 | lylty    | False         |      0.7 |    0.5 |


<a name="binary-features-range"></a>

### Checking the range
The `check_outside_range` method can be used to detect features with data outside the expected range of 0 and 1. Note that the outside of range condition is only possible for binary features encoded as integer data type.

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


<a name="categorical-features"></a>

## Categorical features

### Description
The methods within `CategoricalFeatures` are intended for use with categorical data (data denoting categories). Datasurveyor expects categorical features to be stored as object (string) or integer type. In the example data, `state` and `platform` are categorical features.

<a name="categorical-features-import"></a>

### Importing CategoricalFeatures
The categorical feature tools can be imported with the command below.
```python
from datasurveyor import CategoricalFeatures as CF
```

<a name="categorical-features-mostly-same"></a>

### Checking if values are mostly the same
The `check_mostly_same` method can be used to check if categorical features contain mostly the same value (default threshold 95%). This method can be applied to a single categorical feature or a collection of categorical features.

```python
CF.check_mostly_same(df['state'])
```

|    | mostly_same   |   thresh | most_common   |   count |   prop |
|---:|:--------------|---------:|:--------------|--------:|-------:|
|  0 | False         |     0.95 | WA            |       6 |    0.6 |

```python
CF.check_mostly_same(df[['state', 'platform']])
```

|    | column   | mostly_same   |   thresh | most_common   |   count |   prop |
|---:|:---------|:--------------|---------:|:--------------|--------:|-------:|
|  0 | state    | False         |     0.95 | WA            |       6 |    0.6 |
|  1 | platform | False         |     0.95 | ios           |       5 |    0.5 |

The user can specify whatever threshold is appropriate for their usecase. If `thresh=0.6` is applied, the method will flag features with at least 60% the same value.

```python
CF.check_mostly_same(df['state'], thresh=0.6)
```

|    | mostly_same   |   thresh | most_common   |   count |   prop |
|---:|:--------------|---------:|:--------------|--------:|-------:|
|  0 | True          |      0.6 | WA            |       6 |    0.6 |

```python
CF.check_mostly_same(df[['state', 'platform']], thresh=0.6)
```

|    | column   | mostly_same   |   thresh | most_common   |   count |   prop |
|---:|:---------|:--------------|---------:|:--------------|--------:|-------:|
|  0 | state    | True          |      0.6 | WA            |       6 |    0.6 |
|  1 | platform | False         |      0.6 | ios           |       5 |    0.5 |


<a name="categorical-features-n-categories"></a>

### Checking number of categories
The `n_categories` method can be used to count the number of categories. This method can be applied to a single categorical feature or a collection of categorical features.

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


<a name="general-features"></a>

## General features

### Description
The methods within `GeneralFeatures` are intended for use with any data. Datasurveyor expects inputs to be of type Pandas Series or DataFrame, but has no type expectations for the data within those structures.


<a name="general-features-import"></a>

### Importing GeneralFeatures
The general feature tools can be imported with the command below.

```python
from datasurveyor import GeneralFeatures as GF
```

<a name="general-features-nulls"></a>

### Checking for nulls
The `check_nulls` method can be used to check for nulls. This method can be applied to a single feature or a collection of features.

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


<a name="general-features-fuzzy-nulls"></a>

### Checking for nulls
The `check_fuzzy_nulls` method can be used to check for values that commonly denote nulls. This method can be applied to a single feature or a collection of features.

```python
GF.check_fuzzy_nulls(df['state'])
```

|    | fuzzy_nulls_present   |   fuzzy_null_count |   prop_fuzzy_null |
|---:|:----------------------|-------------------:|------------------:|
|  0 | True                  |                  1 |               0.1 |

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

The defaults items checked for are: 'null', 'Null', 'NULL', '' (empty string), and ' ' (single space). The user can specify additional items to check for using the `add_fuzzy_nulls` argument.

```python
GF.check_fuzzy_nulls(df['state'], add_fuzzy_nulls=['unknown'])
```
|    | fuzzy_nulls_present   |   fuzzy_null_count |   prop_fuzzy_null |
|---:|:----------------------|-------------------:|------------------:|
|  0 | True                  |                  2 |               0.2 |

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


<a name="unique-features"></a>

## Unique features

### Description
The methods within `UniqueFeatures` are intended for use with data where each observation has a unique value. Datasurveyor expects unique features to be stored as datetime, object (string), or integer type. In the example data, `id` is a unique feature.


<a name="unique-features-import"></a>

### Importing UniqueFeatures
The unique feature tools can be imported with the command below.

```python
from datasurveyor import UniqueFeatures as UF
```


<a name="unique-features-uniqueness"></a>

### Checking uniqueness
The `check_uniqueness` method can be used to check if potentially unique features contain unique values. This method can be applied to a single unique feature or a collection of unique features.

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


<a name="datasurveyor-contrib"></a>

## Contributing to datasurveyor
If you are interested in contributing to this project:
1. Fork the [datasurveyor repo](https://github.com/nickbuker/datasurveyor).
1. Clone the forked repository to your machine.
1. Create a git branch.
1. Make changes and push them to GitHub.
1. Submit your changes for review by creating a pull request. In order to be approved changes should include:
    - Appropriate updates to the `README.md`
    - Google style docstrings
    - Tests providing proper coverage of new code


<a name="datasurveyor-test"></a>

## Testing
For those interested in contributing to datasurveyor forking and editing the project, pytest is the testing framework used. To run the tests, create a virtual environment, install the contents of `dev_requirements.txt`, and run the following command from the root directory of the project. The testing scripts can be found in the `tests/` directory.

```bash
$ pytest
```

To run tests and view coverage, use the below command:

```bash
$ pytest --cov=datasurveyor
```
