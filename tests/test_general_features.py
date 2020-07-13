# third party imports
import numpy as np
import pandas as pd
# local imports
from datasurveyor import GeneralFeatures as gf


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


# fail DataFrames for fuzzy nulls
fail_fuzzy_df = pd.DataFrame.from_dict({
    'column': ('b1', 'b2'),
    'fuzzy_nulls_present': (True, False),
    'fuzzy_null_count': (1, 0),
    'prop_fuzzy_null': (0.25, 0.0)
})
fail_fuzzy_ser = pd.DataFrame.from_dict({
    'fuzzy_nulls_present': (True,),
    'fuzzy_null_count': (1,),
    'prop_fuzzy_null': (0.25,),
})


def test_check_nulls_good_df():
    # verifies good data passes the null check
    cols = ['nulls_present', 'null_count', 'prop_null']
    assert not gf.check_nulls(good).loc[:, cols].any(axis=None)


def test_check_nulls_good_ser():
    # verifies good data passes the null check
    cols = ['null_count', 'prop_null']
    assert not gf.check_nulls(good['g1']).loc[:, cols].any(axis=None)


def test_check_nulls_bad_df():
    # verifies that the null check finds rows with nulls
    fail = pd.DataFrame.from_dict({
        'column': ('b1', 'b2'),
        'nulls_present': (True, False),
        'null_count': (1, 0),
        'prop_null': (0.25, 0.0)
    })
    assert fail.equals(gf.check_nulls(bad_nulls1))


def test_check_nulls_bad_ser():
    # verifies that the null check finds rows with nulls
    fail = pd.DataFrame.from_dict({
        'nulls_present': (True,),
        'null_count': (1,),
        'prop_null': (0.25,),
    })
    assert fail.equals(gf.check_nulls(bad_nulls1['b1']))


def test_fuzzy_nulls_good_df():
    # verifies good data passes the null check
    cols = ['fuzzy_nulls_present', 'fuzzy_null_count', 'prop_fuzzy_null']
    assert not gf.check_fuzzy_nulls(good).loc[:, cols].any(axis=None)


def test_fuzzy_nulls_good_ser():
    # verifies good data passes the null check
    cols = ['fuzzy_nulls_present', 'fuzzy_null_count', 'prop_fuzzy_null']
    assert not gf.check_fuzzy_nulls(good['g1']).loc[:, cols].any(axis=None)


def test_fuzzy_nulls_bad1_df():
    # verifies that the fuzzy null check finds rows with fuzzy nulls
    assert fail_fuzzy_df.equals(gf.check_fuzzy_nulls(bad_fuzzy1))


def test_fuzzy_nulls_bad1_ser():
    # verifies that the fuzzy null check finds rows with fuzzy nulls
    assert fail_fuzzy_ser.equals(gf.check_fuzzy_nulls(bad_fuzzy1['b1']))


def test_fuzzy_nulls_bad2_df():
    # verifies that the fuzzy null check finds rows with fuzzy nulls
    assert fail_fuzzy_df.equals(gf.check_fuzzy_nulls(bad_fuzzy2))


def test_fuzzy_nulls_bad2_ser():
    # verifies that the fuzzy null check finds rows with fuzzy nulls
    assert fail_fuzzy_ser.equals(gf.check_fuzzy_nulls(bad_fuzzy2['b1']))


def test_fuzzy_nulls_bad3_df():
    # verifies that the fuzzy null check finds rows with added fuzzy nulls
    assert fail_fuzzy_df.equals(gf.check_fuzzy_nulls(bad_fuzzy3, add_fuzzy_nulls=['foo']))


def test_fuzzy_nulls_bad3_ser():
    # verifies that the fuzzy null check finds rows with added fuzzy nulls
    assert fail_fuzzy_ser.equals(gf.check_fuzzy_nulls(bad_fuzzy3['b1'], add_fuzzy_nulls=['foo']))
