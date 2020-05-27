# third party imports
import numpy as np
import pandas as pd


def validate_dtype(df: pd.DataFrame) -> None:
    """Validates that DataFrame of binary data contains only dtype bool or int.

    Args:
        df: Binary data to be type validated.

    Returns:
        None

    Raises:
        TypeError: If `df` contains dtype other than bool or int
    """
    if not df.dtypes.isin((np.dtype(bool), np.dtype(int))).all():
        raise TypeError('Binary feature columns should be of type bool or int64.')
    return


def check_all_same(df: pd.DataFrame) -> pd.Series:
    """Checks if DataFrame of binary data contains columns where all values are the same.

    Args:
        df: Binary data to be checked if all values are the same.

    Returns:
        Series with index of column names and values of bools indicating if all values are the same.
    """
    validate_dtype(df)
    return df.min(axis=0).eq(df.max(axis=0))


def check_mostly_same(df: pd.DataFrame, thresh: float = 0.95) -> pd.Series:
    """Checks if DataFrame of binary data contains columns where almost all values are the same.

    Args:
        df: Binary data to be checked if almost all values are the same.
        thresh: Threshold for what proportion of data must be the same to fail check.

    Returns:
        Series with index of column names and values of bools indicating if almost all values are the same.

    Raises:
        ValueError: If `thresh` less than or equal to 0.0 or greater than or equal to 1.0.
    """
    if thresh >= 1.0 or thresh <= 0.0:
        raise ValueError('The thresh parameter must be greater than 0.0 and less than 1.0.')
    validate_dtype(df)
    means = df.mean(axis=0)
    return (means >= thresh) | (means <= 1 - thresh)


def check_range(df: pd.DataFrame) -> pd.Series:
    """Checks if DataFrame of binary data contains columns where min is less than 0 or max is greater than 1.
    
    Args:
        df: Binary data to be checked if all values are less than 0 or greater than 1.

    Returns:
        Series with index of column names and values of bools indicating whether min or max is outside of range.
    """
    validate_dtype(df)
    return (df.min(axis=0) < 0) | (df.max(axis=0) > 1)
