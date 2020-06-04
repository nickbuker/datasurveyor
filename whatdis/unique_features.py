# third party imports
import numpy as np
import pandas as pd


def validate_dtype(df: pd.DataFrame) -> None:
    """Validates that DataFrame of unique data contains only dtype object, int, or datetime.

    Args:
        df: Unique data to be validated.

    Returns:
        None

    Raises:
        TypeError: If `df` contains dtype other than object, int, or datetime.
    """
    if not df.dtypes.isin((np.dtype('O'), np.dtype(int), np.dtype('datetime64[ns]'))).all():
        raise TypeError('Unique feature columns should be of type object, int64, or datetime64.')
    return


def check_uniqueness(df: pd.DataFrame, counts: bool = False) -> pd.Series:
    """Checks if DataFrame contains columns with duplicates.

    Args:
        df: Data to be checked for duplicates.
        counts: If True, returns counts of duplicates, if False, returns boolean indicators of duplicates.

    Returns:
        Series with index of column names and values of duplicate counts if `counts` is True, or
        bools indicating presence of duplicates if `counts` is False.
    """
    validate_dtype(df)
    dupes = df.nunique(axis=0).subtract(df.shape[0]).multiply(-1)
    if not counts:
        dupes = dupes.astype(bool)
    return dupes
