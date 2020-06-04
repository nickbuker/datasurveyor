# third party imports
import numpy as np
import pandas as pd


def validate_dtype(df: pd.DataFrame) -> None:
    """TODO

    Args:
        df:

    Returns:

    """
    if not df.dtypes.isin((np.dtype('O'), np.dtype(int), np.dtype('datetime64[ns]'))).all():
        raise TypeError('Unique feature columns should be of type object, int64, or datetime64.')
    return


def check_uniqueness(df: pd.DataFrame, counts: bool = False) -> pd.Series:
    """ TODO

    Args:
        df:
        counts:

    Returns:

    """
    validate_dtype(df)
    dupes = df.nunique(axis=0).subtract(df.shape[0]).multiply(-1)
    if not counts:
        dupes = dupes.astype(bool)
    return dupes
