# third party imports
import pandas as pd
# local imports
import whatdis.unique_features as uf


# should pass all checks
good = pd.DataFrame.from_dict({
    'g1': ('foo', 'bar', 'baz', 'boo'),
    'g2': (0, 1, 2, 4),
    'g3': ('I', 'like', 'peperoni', 'pizza'),
})

# should fail duplicates test
bad = pd.DataFrame.from_dict({
    'b1': (0, 1, 0, 1),
    'b2': ('foo', 'bar', 'baz', 'boo'),
})

# series that should match output of failed checks
fail_series_bool = pd.Series([True, False], index=['b1', 'b2'])
fail_series_counts = pd.Series([2, 0], index=['b1', 'b2'])

def test_check_uniqueness_good_bool():
    # TODO comment
    assert not uf.check_uniqueness(good, counts=False).any()


def test_check_uniqueness_good_counts():
    # TODO comment
    assert uf.check_uniqueness(good, counts=True).max() == 0


def test_check_uniques_bad_bool():
    # TODO comment
    assert uf.check_uniqueness(bad, counts=False).equals(fail_series_bool)


def test_check_uniques_bad_counts():
    # TODO comment
    assert uf.check_uniqueness(bad, counts=True).equals(fail_series_counts)
