# third party imports
import numpy as np
import pandas as pd
import pytest
# local imports
from whatdis import categorical_features as cf


# should pass all checks
good = pd.DataFrame.from_dict({
    'g1': ('a', 'b', 'c', 'd'),
    'g2': (0, 1, 1, 0),
})


nan = pd.DataFrame.from_dict({
    'g1': (np.nan, np.nan, 'a', 'b'),
    'g2': (0, 1, 2, 3),
})

# should fail dtype validation
bad_type = pd.DataFrame.from_dict({
    'b1': (True, True, False, True),
    'b2': (1.0, 0.0, 1.0, 0.0),
})


# series that should match output of check_n_categories
good_ser = pd.Series([4, 2], index=['g1', 'g2'])
drop_nan_ser = pd.Series([2, 4], index=['g1', 'g2'])
nan_ser = pd.Series([3, 4], index=['g1', 'g2'])


def test_validate_categorical_dtype_good_df():
    # verifies good data passes the dtype check
    cf.validate_categorical_dtype(good)


def test_validate_categorical_dtype_good_ser():
    # verifies good data passes the dtype check
    cf.validate_categorical_dtype(good['g1'])


def test_validate_categorical_dtype_bad_df():
    # checks that TypeError is raised when df contains float data
    with pytest.raises(TypeError) as excinfo:
        cf.validate_categorical_dtype(bad_type)
    # verifies TypeError contains appropriate message
    assert 'should be of type object or int64' in str(excinfo.value)


def test_validate_categorical_dtype_bad_ser():
    # checks that TypeError is raised when df contains float data
    with pytest.raises(TypeError) as excinfo:
        cf.validate_categorical_dtype(bad_type['b1'])
    # verifies TypeError contains appropriate message
    assert 'should be of type object or int64' in str(excinfo.value)


def test_check_n_categories_df():
    # verifies that check_n_categories generates the expected output
    assert good_ser.equals(cf.check_n_categories(good))


def test_check_n_categories_ser():
    # verifies that check_n_categories generates the expected output
    assert good_ser[1] == cf.check_n_categories(good['g2'])


def test_check_n_categories_dropna_df():
    # verifies that check_n_categories generates the expected output with nulls
    assert drop_nan_ser.equals(cf.check_n_categories(nan, dropna=True))


def test_check_n_categories_no_dropna_df():
    # verifies that check_n_categories generates the expected output with nulls
    assert nan_ser.equals(cf.check_n_categories(nan, dropna=False))


def test_check_n_categories_dropna_ser():
    # verifies that check_n_categories generates the expected output with nulls
    assert drop_nan_ser[0] == cf.check_n_categories(nan['g1'], dropna=True)


def test_check_n_categories_no_dropna_ser():
    # verifies that check_n_categories generates the expected output with nulls
    assert nan_ser[0] == cf.check_n_categories(nan['g1'], dropna=False)
