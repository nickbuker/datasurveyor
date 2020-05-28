# third party imports
import pandas as pd
import pytest
# local imports
import whatdis.binary_features as bf


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

# series that should match output of failed checks
fail_series = pd.Series([True, False], index=['b1', 'b2'])


def test_validate_dtype_good():
    # verifies good data passes the dtype check
    bf.validate_dtype(good)


def test_validate_dtype_bad_str():
    # checks that TypeError is raised when df contains object (str) data
    with pytest.raises(TypeError) as excinfo:
        bf.validate_dtype(bad_type1)
    # verifies TypeError contains appropriate message
    assert 'should be of type bool or int64' in str(excinfo.value)


def test_validate_dtype_bad_float():
    # checks that TypeError is raised when df contains float data
    with pytest.raises(TypeError) as excinfo:
        bf.validate_dtype(bad_type2)
    # verifies TypeError contains appropriate message
    assert 'should be of type bool or int64' in str(excinfo.value)


def test_check_all_same_good():
    # verifies good data passes the all same check
    assert not bf.check_all_same(good).any()


def test_check_all_same_bad():
    # verifies that the all same check finds rows with all the same value
    assert fail_series.equals(bf.check_all_same(bad_same1))


def test_check_mostly_same_good():
    # verifies good data passes the mostly same check
    assert not bf.check_mostly_same(good).any()


def test_check_mostly_same_bad1():
    # verifies that the mostly same check finds rows with mostly the same value
    assert fail_series.equals(bf.check_mostly_same(bad_same2, 0.7))


def test_check_range_good():
    # verifies good data passes the range check
    assert not bf.check_range(good).any()


def test_check_range_bad1():
    # verifies that the range check finds rows with low values
    assert fail_series.equals(bf.check_range(bad_range1))


def test_check_range_bad2():
    # verifies that the range check finds rows with high values
    assert fail_series.equals(bf.check_range(bad_range2))
