# standard library imports
from typing import List, Optional
# third party imports
import pandas as pd


def check_nulls(df: pd.DataFrame, counts: bool = False) -> pd.Series:
    """Checks if DataFrame contains columns with nulls.

    Args:
        df: Data to be checked for nulls.
        counts: If True, returns counts of nulls, if False, returns boolean indicators of nulls.

    Returns:
        Series with index of column names and values null counts if `counts` is True, or bools indicating
        presence of nulls if `counts` is False.
    """
    if counts:
        nulls = df.isna().sum(axis=0)
    else:
        nulls = df.isna().any(axis=0)
    return nulls


def check_fuzzy_nulls(
        df: pd.DataFrame,
        add_fuzzy_nulls: Optional[List] = None,
        counts: bool = False,
) -> pd.Series:
    """Checks if DataFrame contains columns with fuzzy nulls.

    Args:
        df: Data to be checked for fuzzy nulls.
        add_fuzzy_nulls: Additional items to check as fuzzy nulls.
        counts: If True, returns counts of fuzzy nulls, if False, returns boolean indicators of fuzzy nulls.

    Returns:
        Series with index of column names and values fuzzy null counts if `counts` is True, or bools
        indicating presence of fuzzy nulls if `counts` is False.
    """
    fuzzy_nulls = ['null', 'Null', 'NULL', '', ' ']
    if add_fuzzy_nulls is not None:
        fuzzy_nulls.extend(add_fuzzy_nulls)
    if counts:
        nulls = df.isin(fuzzy_nulls).sum(axis=0)
    else:
        nulls = df.isin(fuzzy_nulls).any(axis=0)
    return nulls
