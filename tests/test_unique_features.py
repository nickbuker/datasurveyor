# TODO make compatible with pandas Series
# third party imports
import numpy as np
import pandas as pd
import pytest
# local imports
import whatdis.unique_features as uf


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

# series that should match output of failed checks
fail_series_bool = pd.Series([True, False], index=['b1', 'b2'])
fail_series_counts = pd.Series([2, 0], index=['b1', 'b2'])


def test_validate_dtype_good():
    # verifies good data passes the dtype check
    uf.validate_dtype(good)


def test_validate_dtype_bad():
    # checks that TypeError is raised when df contains float data
    with pytest.raises(TypeError) as excinfo:
        uf.validate_dtype(bad_type)
    # verifies TypeError contains appropriate message
    assert 'should be of type object, int64, or datetime64' in str(excinfo.value)


def test_check_uniqueness_good_bool():
    # verifies that good data passes uniqueness check (bool)
    assert not uf.check_uniqueness(good, counts=False).any()


def test_check_uniqueness_good_counts():
    # verifies that good data passes uniqueness check (counts)
    assert uf.check_uniqueness(good, counts=True).max() == 0


def test_check_uniques_bad_bool():
    # verifies that the uniqueness check find duplicates (bool)
    assert uf.check_uniqueness(bad_unique, counts=False).equals(fail_series_bool)


def test_check_uniques_bad_counts():
    # verifies that the uniqueness check finds duplicates (counts)
    assert uf.check_uniqueness(bad_unique, counts=True).equals(fail_series_counts)
