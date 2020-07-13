# third party imports
import pandas as pd
import pytest
# local imports
from datasurveyor import BinaryFeatures as bf


# should pass all checks
good = pd.DataFrame.from_dict({
    'g1': (True, False, True, False),
    'g2': (0, 1, 0, 1),
    'g3': (False, True, False, True),
})

# should fail dtype check due to strings
bad_type1 = pd.DataFrame.from_dict({
    'b1': ('True', 'True', 'False', 'True'),
    'b2': (False, True, False, True),
})

# should fail dtype check due to floats
bad_type2 = pd.DataFrame.from_dict({
    'b1': (1.0, 0.0, 0.6, 0.9),
    'b2': (False, True, False, True),
})

# should fail all same check
bad_same1 = pd.DataFrame.from_dict({
    'b1': (1, 1, 1, 1),
    'b2': (False, True, False, True),
})

# should fail mostly same check with threshold 0.7
bad_same2 = pd.DataFrame.from_dict({
    'b1': (True, True, True, False),
    'b2': (False, True, False, True),
})

# should fail range check (less than 0)
bad_range1 = pd.DataFrame.from_dict({
    'b1': (1, 0, 0, -1),
    'b2': (False, True, False, True),
})

# should fail range check (greater than 1)
bad_range2 = pd.DataFrame.from_dict({
    'b1': (1, 0, 10, 1),
    'b2': (False, True, False, True),
})


def test_validate_dtype_good_df():
    # verifies good data passes the dtype check
    bf._validate_binary_dtype(good)


def test_validate_dtype_good_ser():
    # verifies good data passes the dtype check
    bf._validate_binary_dtype(good['g1'])


def test_validate_dtype_bad_str_df():
    # checks that TypeError is raised when df contains object (str) data
    with pytest.raises(TypeError) as excinfo:
        bf._validate_binary_dtype(bad_type1)
    # verifies TypeError contains appropriate message
    assert 'should be of type bool or int64' in str(excinfo.value)


def test_validate_dtype_bad_str_ser():
    # checks that TypeError is raised when series contains object (str) data
    with pytest.raises(TypeError) as excinfo:
        bf._validate_binary_dtype(bad_type1['b1'])
    # verifies TypeError contains appropriate message
    assert 'should be of type bool or int64' in str(excinfo.value)


def test_validate_dtype_bad_float_df():
    # checks that TypeError is raised when df contains float data
    with pytest.raises(TypeError) as excinfo:
        bf._validate_binary_dtype(bad_type2)
    # verifies TypeError contains appropriate message
    assert 'should be of type bool or int64' in str(excinfo.value)


def test_validate_dtype_bad_float_ser():
    # checks that TypeError is raised when series contains float data
    with pytest.raises(TypeError) as excinfo:
        bf._validate_binary_dtype(bad_type2['b1'])
    # verifies TypeError contains appropriate message
    assert 'should be of type bool or int64' in str(excinfo.value)


def test_check_all_same_good_df():
    # verifies good data passes the all same check
    assert not bf.check_all_same(good).loc[:, 'all_same'].any()


def test_check_all_same_good_ser():
    # verifies good data passes the all same check
    assert not bf.check_all_same(good['g1']).loc[:, 'all_same'].any()


def test_check_all_same_bad_df():
    # verifies that the all same check finds rows with all the same value
    fail = pd.DataFrame.from_dict({'column': ('b1', 'b2'), 'all_same': (True, False)})
    assert fail.equals(bf.check_all_same(bad_same1))


def test_check_all_same_bad_ser():
    # verifies that the all same check finds rows with all the same value
    fail = pd.DataFrame.from_dict({'all_same': (True,)})
    assert fail.equals(bf.check_all_same(bad_same1['b1']))


def test_check_mostly_same_good_df():
    # verifies good data passes the mostly same check
    assert not bf.check_mostly_same(good).loc[:, 'mostly_same'].any(axis=0)


def test_check_mostly_same_good_ser():
    # verifies good data passes the mostly same check
    assert not bf.check_mostly_same(good['g1']).loc[:, 'mostly_same'].any()


def test_check_mostly_same_bad1_df():
    # verifies that the mostly same check finds rows with mostly the same value
    fail = pd.DataFrame.from_dict({
        'column': ('b1', 'b2'),
        'mostly_same': (True, False),
        'thresh': (0.7, 0.7),
        'mean': (0.75, 0.5),
    })
    assert fail.equals(bf.check_mostly_same(bad_same2, 0.7))


def test_check_mostly_same_bad1_ser():
    # verifies that the mostly same check finds rows with mostly the same value
    fail = pd.DataFrame.from_dict({
        'mostly_same': (True,),
        'thresh': (0.7,),
        'mean': (0.75,),
    })
    assert fail.equals(bf.check_mostly_same(bad_same2['b1'], 0.7))


def test_check_outside_range_good_df():
    # verifies good data passes the range check
    assert not bf.check_outside_range(good).loc[:, 'outside_range'].any(axis=0)


def test_check_range_good_ser():
    # verifies good data passes the range check
    assert not bf.check_outside_range(good['g1']).loc[:, 'outside_range'].any()


def test_check_range_bad1_df():
    # verifies that the range check finds rows with low values
    fail = pd.DataFrame.from_dict({'column': ('b1', 'b2'), 'outside_range': (True, False)})
    assert fail.equals(bf.check_outside_range(bad_range1))


def test_check_range_bad1_ser():
    # verifies that the range check finds rows with low values
    fail = pd.DataFrame.from_dict({'outside_range': (True,)})
    assert fail.equals(bf.check_outside_range(bad_range1['b1']))


def test_check_range_bad2_df():
    # verifies that the range check finds rows with high values
    fail = pd.DataFrame.from_dict({'column': ('b1', 'b2'), 'outside_range': (True, False)})
    assert fail.equals(bf.check_outside_range(bad_range2))


def test_check_range_bad2_ser():
    # verifies that the range check finds rows with high values
    fail = pd.DataFrame.from_dict({'outside_range': (True,)})
    assert fail.equals(bf.check_outside_range(bad_range2['b1']))
