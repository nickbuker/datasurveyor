# TODO: look into null ints
# TODO: limit fuzzy checks via dtype selection
# standard library imports
from typing import List, Optional
# third party imports
import numpy as np
import pandas as pd


# should fail all same check
bad_nulls1 = pd.DataFrame.from_dict({
    'b1': ('True', 'Null', 'True', 'False'),
    'b2': (1, 0, 1, 0),
})


def check_nulls(df: pd.DataFrame, counts: bool = False) -> pd.Series:
    """Check if DataFrame contains columns with nulls

    Args:
        df: Data to be checked for nulls.
        counts: If True, returns counts of nulls, if False, returns boolean indicators of nulls.

    Returns:
        Series with index of column names and values null counts if `counts` is True or bools indicating
        presence of nulls if `counts` is False.
    """
    if counts:
        nulls = df.isna().sum(axis=0)
    else:
        nulls = df.isna().any(axis=0)
    return nulls


def check_fuzzy_nulls(
        df: pd.DataFrame,
        add_fuzzy_nulls: Optional[List[str]] = None,
        counts: bool = False,
) -> pd.Series:
    """

    Args:
        df:
        add_fuzzy_nulls:
        counts:

    Returns:

    """
    fuzzy_nulls = ['null', 'Null', 'NA', '', ' ']
    if add_fuzzy_nulls is not None:
        fuzzy_nulls.extend(add_fuzzy_nulls)
    if counts:
        nulls = df.isin(fuzzy_nulls).sum(axis=0)
    else:
        nulls = df.isin(fuzzy_nulls).any(axis=0)
    return nulls


if __name__ == '__main__':
    print(check_fuzzy_nulls(bad_nulls1, counts=False))
