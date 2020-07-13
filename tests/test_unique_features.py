# third party imports
import numpy as np
import pandas as pd
import pytest
# local imports
from datasurveyor import UniqueFeatures as uf


# should pass all checks
good = pd.DataFrame.from_dict({
    'g1': ('foo', 'bar', 'baz', 'boo'),
    'g2': (0, 1, 2, 4),
    'g3': (np.datetime64('2017-01-01'), np.datetime64('2018-01-01'),
           np.datetime64('2019-01-01'), np.datetime64('2020-01-01')),
})

# should fail dtype test
bad_type = pd.DataFrame.from_dict({
    'b1': (0.0, 1.0, 2.0, 4.0),
    'b2': ('foo', 'bar', 'baz', 'boo'),
})

# should fail duplicates test
bad_unique = pd.DataFrame.from_dict({
    'b1': (0, 1, 0, 1),
    'b2': ('foo', 'bar', 'baz', 'boo'),
})

# should raise ValueError
bad_unique_nan = pd.DataFrame.from_dict({
    'b1': ('foo', 'bar', 'baz', np.nan),
    'b2': (0, 1, 2, 3),
})

# fail DataFrames for fuzzy nulls
fail_dupe_df = pd.DataFrame.from_dict({
    'column': ('b1', 'b2'),
    'dupes_present': (True, False),
    'dupe_count': (2, 0),
    'prop_dupe': (0.5, 0.0)
})
fail_dupe_ser = pd.DataFrame.from_dict({
    'dupes_present': (True,),
    'dupe_count': (2,),
    'prop_dupe': (0.5,),
})


def test_validate_dtype_good_df():
    # verifies good data passes the dtype check
    uf._validate_unique_dtype(good)


def test_validate_dtype_good_ser():
    # verifies good data passes the dtype check
    uf._validate_unique_dtype(good['g1'])


def test_validate_dtype_bad_df():
    # checks that TypeError is raised when df contains float data
    with pytest.raises(TypeError) as excinfo:
        uf._validate_unique_dtype(bad_type)
    # verifies TypeError contains appropriate message
    assert 'should be of type object, int64, or datetime64' in str(excinfo.value)


def test_validate_dtype_bad_ser():
    # checks that TypeError is raised when df contains float data
    with pytest.raises(TypeError) as excinfo:
        uf._validate_unique_dtype(bad_type['b1'])
    # verifies TypeError contains appropriate message
    assert 'should be of type object, int64, or datetime64' in str(excinfo.value)


def test_detect_nan_df():
    # checks that TypeError is raised when df contains object (str) data
    with pytest.raises(ValueError) as excinfo:
        uf.check_uniqueness(bad_unique_nan)
    # verifies TypeError contains appropriate message
    assert 'should not contain nulls' in str(excinfo.value)


def test_detect_nan_ser():
    # checks that TypeError is raised when df contains object (str) data
    with pytest.raises(ValueError) as excinfo:
        uf.check_uniqueness(bad_unique_nan['b1'])
    # verifies TypeError contains appropriate message
    assert 'should not contain nulls' in str(excinfo.value)


def test_check_uniqueness_good_df():
    # verifies that good data passes uniqueness check (bool)
    cols = ['dupes_present', 'dupe_count', 'prop_dupe']
    assert not uf.check_uniqueness(good).loc[:, cols].any(axis=None)


def test_check_uniqueness_good_ser():
    # verifies that good data passes uniqueness check (bool)
    cols = ['dupes_present', 'dupe_count', 'prop_dupe']
    assert not uf.check_uniqueness(good['g1']).loc[:, cols].any(axis=None)


def test_check_uniques_bad_df():
    # verifies that the uniqueness check find duplicates (bool)
    assert fail_dupe_df.equals(uf.check_uniqueness(bad_unique))


def test_check_uniques_bad_ser():
    # verifies that the uniqueness check find duplicates (bool)
    assert fail_dupe_ser.equals(uf.check_uniqueness(bad_unique['b1']))
