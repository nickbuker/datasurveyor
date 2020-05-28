# third party imports
import numpy as np
import pandas as pd
# local imports
import whatdis.general_features as gf


# should pass all checks
good = pd.DataFrame.from_dict({
    'g1': (True, False, True, False),
    'g2': (0, 1, 0, 1),
    'g3': (False, True, False, True),
})

# should fail null check
bad_nulls1 = pd.DataFrame.from_dict({
    'b1': (True, np.NaN, False, True),
    'b2': (1, 0, 1, 0),
})

# should fail fuzzy null check
bad_fuzzy1 = pd.DataFrame.from_dict({
    'b1': ('True', '', 'False', 'True'),
    'b2': (1, 0, 1, 0),
})

# should fail fuzzy null check
bad_fuzzy2 = pd.DataFrame.from_dict({
    'b1': ('True', 'NA', 'False', 'True'),
    'b2': (1, 0, 1, 0),
})


# series that should match output of failed checks
fail_series_bool = pd.Series([True, False], index=['b1', 'b2'])
fail_series_counts = pd.Series([1, 0], index=['b1', 'b2'])


def test_check_nulls_good():
    # verifies good data passes the null check
    assert not gf.check_nulls(good).any(axis=0)


def test_check_nulls_bad_bool():
    # verifies that the null check finds rows with nulls
    assert fail_series_bool.equals(gf.check_nulls(bad_nulls1, counts=False))


def test_check_nulls_bad_counts():
    # verifies that the null check counts nulls in each row
    assert fail_series_counts.equals(gf.check_nulls(bad_nulls1, counts=True))


def test_fuzzy_nulls_good():
    # verifies good data passes the null check
    assert not gf.check_fuzzy_nulls(good).any(axis=0)


def test_fuzzy_nulls_bad1_bool():
    # verifies that the fuzzy null check finds rows with fuzzy nulls
    assert fail_series_bool.equals(gf.check_fuzzy_nulls(bad_fuzzy1, counts=False))


def test_fuzzy_nulls_bad1_count():
    # verifies that the fuzzy null check counts fuzzy nulls in each row
    assert fail_series_counts.equals(gf.check_fuzzy_nulls(bad_fuzzy1, counts=True))


def test_fuzzy_nulls_bad2_bool():
    # verifies that the fuzzy null check finds rows with fuzzy nulls
    assert fail_series_bool.equals(gf.check_fuzzy_nulls(bad_fuzzy2, counts=False))


def test_fuzzy_nulls_bad2_count():
    # verifies that the fuzzy null check counts fuzzy nulls in each row
    assert fail_series_counts.equals(gf.check_fuzzy_nulls(bad_fuzzy2, counts=True))