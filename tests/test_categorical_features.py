# third party imports
import numpy as np
import pandas as pd
import pytest
# local imports
from datasurveyor import CategoricalFeatures as cf


# should pass all checks
good = pd.DataFrame.from_dict({
    'g1': ('a', 'b', 'c', 'd'),
    'g2': (0, 1, 1, 0),
})

# used to test behavior of data with nan's
nan = pd.DataFrame.from_dict({
    'g1': (np.nan, np.nan, 'a', 'b'),
    'g2': (0, 1, 2, 3),
})

# should fail dtype validation
bad_type = pd.DataFrame.from_dict({
    'b1': (True, True, False, True),
    'b2': (1.0, 0.0, 1.0, 0.0),
})

# DataFrames that should match output of check_n_categories
mostly_same_out1 = pd.DataFrame.from_dict({
    'column': ('g1', 'g2'),
    'mostly_same': (False, True),
    'thresh': (0.4, 0.4),
    'most_common': ('a', 0),
    'count': (1, 2),
    'prop': (0.25, 0.5),
})
# DataFrames that should match output of check_n_categories
mostly_same_out2 = pd.DataFrame.from_dict({
    'mostly_same': (True,),
    'thresh': (0.4,),
    'most_common': (0,),
    'count': (2,),
    'prop': (0.5,),
})
good_result = pd.DataFrame.from_dict({
    'column': ('g1', 'g2'),
    'n_categories': (4, 2)
})
drop_nan_result = pd.DataFrame.from_dict({
    'column': ('g1', 'g2'),
    'n_categories': (2, 4)
})
nan_result = pd.DataFrame.from_dict({
    'column': ('g1', 'g2'),
    'n_categories': (3, 4)
})


def test_validate_categorical_dtype_good_df():
    # verifies good data passes the dtype check
    cf._validate_categorical_dtype(good)


def test_validate_categorical_dtype_good_ser():
    # verifies good data passes the dtype check
    cf._validate_categorical_dtype(good['g1'])


def test_validate_categorical_dtype_bad_df():
    # checks that TypeError is raised when df contains float data
    with pytest.raises(TypeError) as excinfo:
        cf._validate_categorical_dtype(bad_type)
    # verifies TypeError contains appropriate message
    assert 'should be of type object or int64' in str(excinfo.value)


def test_validate_categorical_dtype_bad_ser():
    # checks that TypeError is raised when df contains float data
    with pytest.raises(TypeError) as excinfo:
        cf._validate_categorical_dtype(bad_type['b1'])
    # verifies TypeError contains appropriate message
    assert 'should be of type object or int64' in str(excinfo.value)


def test_mostly_same_df():
    # verifies mostly same output matches expectation
    assert mostly_same_out1.equals(cf.check_mostly_same(good, thresh=0.4))


def test_mostly_same_ser():
    # verifies mostly same output matches expectation
    cols = ['mostly_same', 'thresh', 'most_common', 'count', 'prop']
    assert mostly_same_out2.equals(cf.check_mostly_same(good['g2'], thresh=0.4))


def test_check_n_categories_df():
    # verifies that check_n_categories generates the expected output
    assert good_result.equals(cf.check_n_categories(good))


def test_check_n_categories_ser():
    # verifies that check_n_categories generates the expected output
    assert good_result.loc[1, 'n_categories'] == cf.check_n_categories(good['g2']).values


def test_check_n_categories_dropna_df():
    # verifies that check_n_categories generates the expected output with nulls
    assert drop_nan_result.equals(cf.check_n_categories(nan, dropna=True))


def test_check_n_categories_no_dropna_df():
    # verifies that check_n_categories generates the expected output with nulls
    assert nan_result.equals(cf.check_n_categories(nan, dropna=False))


def test_check_n_categories_dropna_ser():
    # verifies that check_n_categories generates the expected output with nulls
    assert drop_nan_result.loc[0, 'n_categories'] == cf.check_n_categories(nan['g1'], dropna=True).values


def test_check_n_categories_no_dropna_ser():
    # verifies that check_n_categories generates the expected output with nulls
    assert nan_result.loc[0, 'n_categories'] == cf.check_n_categories(nan['g1'], dropna=False).values
