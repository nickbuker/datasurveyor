# third party imports
import pandas as pd
import pytest
# local imports
import whatdis.binary_features as bf


good = pd.DataFrame.from_dict({
    'g1': (True, False, True, False),
    'g2': (0, 1, 0, 1),
    'g3': (False, True, False, True),
})

bad_type1 = pd.DataFrame.from_dict({
    'b1': ('True', 'True', 'False', 'True'),
    'b2': (False, True, False, True),
})

bad_type2 = pd.DataFrame.from_dict({
    'b1': (1.0, 0.0, 0.6, 0.9),
    'b2': (False, True, False, True),
})

bad_same1 = pd.DataFrame.from_dict({
    'b1': (1, 1, 1, 1),
    'b2': (False, True, False, True),
})

bad_same2 = pd.DataFrame.from_dict({
    'b1': (True, True, True, False),
    'b2': (False, True, False, True),
})

bad_range1 = pd.DataFrame.from_dict({
    'b1': (1, 0, 0, -1),
    'b2': (False, True, False, True),
})

bad_range2 = pd.DataFrame.from_dict({
    'b1': (1, 0, 10, 1),
    'b2': (False, True, False, True),
})


fail_series = pd.Series([True, False], index=['b1', 'b2'])


def test_validate_dtype_good():
    bf.validate_dtype(good)


def test_validate_dtype_bad_str():
    with pytest.raises(TypeError) as excinfo:
        bf.validate_dtype(bad_type1)
    assert 'should be of type bool or int64' in str(excinfo.value)


def test_validate_dtype_bad_float():
    with pytest.raises(TypeError) as excinfo:
        bf.validate_dtype(bad_type2)
    assert 'should be of type bool or int64' in str(excinfo.value)


def test_check_all_same_good():
    assert not bf.check_all_same(bad_same1).all()


def test_check_all_same_bad():
    assert fail_series.equals(bf.check_all_same(bad_same1))


def test_check_mostly_same_good():
    assert not bf.check_mostly_same(good).all()


def test_check_mostly_same_bad1():
    assert fail_series.equals(bf.check_mostly_same(bad_same2, 0.7))


def test_check_range_good():
    assert not bf.check_range(good).all()


def test_check_range_bad1():
    assert fail_series.equals(bf.check_range(bad_range1))


def test_check_range_bad2():
    assert fail_series.equals(bf.check_range(bad_range2))
