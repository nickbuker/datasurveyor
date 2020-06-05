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
    'b1': ('True', 'NULL', 'False', 'True'),
    'b2': (1, 0, 1, 0),
})

# should fail fuzzy null check with added fuzzy
bad_fuzzy3 = pd.DataFrame.from_dict({
    'b1': ('True', 'foo', 'False', 'True'),
    'b2': (1, 0, 1, 0),
})

# series that should match output of failed checks
fail_series_bool = pd.Series([True, False], index=['b1', 'b2'])
fail_series_counts = pd.Series([1, 0], index=['b1', 'b2'])


def test_check_nulls_good_bool_df():
    # verifies good data passes the null check
    assert not gf.check_nulls(good).any(axis=0)


def test_check_nulls_good_bool_ser():
    # verifies good data passes the null check
    assert not gf.check_nulls(good['g1'])


def test_check_nulls_good_count_df():
    # verifies good data passes the null check
    assert gf.check_nulls(good, counts=True).sum(axis=0) == 0


def test_check_nulls_good_count_ser():
    # verifies good data passes the null check
    assert gf.check_nulls(good['g1'], counts=True) == 0


def test_check_nulls_bad_bool_df():
    # verifies that the null check finds rows with nulls
    assert fail_series_bool.equals(gf.check_nulls(bad_nulls1, counts=False))


def test_check_nulls_bad_bool_ser():
    # verifies that the null check finds rows with nulls
    assert fail_series_bool['b1'] == gf.check_nulls(bad_nulls1['b1'], counts=False)


def test_check_nulls_bad_counts_df():
    # verifies that the null check counts nulls in each row
    assert fail_series_counts.equals(gf.check_nulls(bad_nulls1, counts=True))


def test_check_nulls_bad_counts_ser():
    # verifies that the null check counts nulls in each row
    assert fail_series_counts['b1'] == gf.check_nulls(bad_nulls1['b1'], counts=True)


def test_fuzzy_nulls_good_df():
    # verifies good data passes the null check
    assert not gf.check_fuzzy_nulls(good).any(axis=0)


def test_fuzzy_nulls_good_ser():
    # verifies good data passes the null check
    assert not gf.check_fuzzy_nulls(good['g1'])


def test_fuzzy_nulls_bad1_bool_df():
    # verifies that the fuzzy null check finds rows with fuzzy nulls
    assert fail_series_bool.equals(gf.check_fuzzy_nulls(bad_fuzzy1, counts=False))


def test_fuzzy_nulls_bad1_bool_ser():
    # verifies that the fuzzy null check finds rows with fuzzy nulls
    assert fail_series_bool['b1'] == gf.check_fuzzy_nulls(bad_fuzzy1['b1'], counts=False)


def test_fuzzy_nulls_bad1_count_df():
    # verifies that the fuzzy null check counts fuzzy nulls in each row
    assert fail_series_counts.equals(gf.check_fuzzy_nulls(bad_fuzzy1, counts=True))


def test_fuzzy_nulls_bad1_count_ser():
    # verifies that the fuzzy null check counts fuzzy nulls in each row
    assert fail_series_counts['b1'] == gf.check_fuzzy_nulls(bad_fuzzy1['b1'], counts=True)


def test_fuzzy_nulls_bad2_bool_df():
    # verifies that the fuzzy null check finds rows with fuzzy nulls
    assert fail_series_bool.equals(gf.check_fuzzy_nulls(bad_fuzzy2, counts=False))


def test_fuzzy_nulls_bad2_bool_ser():
    # verifies that the fuzzy null check finds rows with fuzzy nulls
    assert fail_series_bool['b1'] == gf.check_fuzzy_nulls(bad_fuzzy2['b1'], counts=False)


def test_fuzzy_nulls_bad2_count_df():
    # verifies that the fuzzy null check counts fuzzy nulls in each row
    assert fail_series_counts.equals(gf.check_fuzzy_nulls(bad_fuzzy2, counts=True))


def test_fuzzy_nulls_bad2_count_ser():
    # verifies that the fuzzy null check counts fuzzy nulls in each row
    assert fail_series_counts['b1'] == gf.check_fuzzy_nulls(bad_fuzzy2['b1'], counts=True)


def test_fuzzy_nulls_bad3_bool_df():
    # verifies that the fuzzy null check finds rows with added fuzzy nulls
    assert fail_series_bool.equals(gf.check_fuzzy_nulls(bad_fuzzy3, add_fuzzy_nulls=['foo'], counts=False))


def test_fuzzy_nulls_bad3_bool_ser():
    # verifies that the fuzzy null check finds rows with added fuzzy nulls
    assert fail_series_bool['b1'] == gf.check_fuzzy_nulls(bad_fuzzy3['b1'], add_fuzzy_nulls=['foo'], counts=False)


def test_fuzzy_nulls_bad3_count_df():
    # verifies that the fuzzy null check counts added fuzzy nulls in each row
    assert fail_series_counts.equals(gf.check_fuzzy_nulls(bad_fuzzy3, add_fuzzy_nulls=['foo'],  counts=True))


def test_fuzzy_nulls_bad3_count_ser():
    # verifies that the fuzzy null check counts added fuzzy nulls in each row
    assert fail_series_counts['b1'] == gf.check_fuzzy_nulls(bad_fuzzy3['b1'], add_fuzzy_nulls=['foo'],  counts=True)
