# standard library imports
from typing import Union
# third party imports
import numpy as np
import pandas as pd
# local imports
from whatdis import utils


def validate_dtype(data: Union[pd.DataFrame, pd.Series]) -> None:
    """Validates that unique data contains only dtype object, int, or datetime.

    Args:
        data: Unique data to be validated.

    Returns:
        None

    Raises: TODO
        TypeError: If `df` contains dtype other than object, int, or datetime.
    """
    is_df = utils.check_if_df(data)
    err_message = 'Unique feature columns should be of type object, int64, or datetime64.'
    types = (np.dtype('O'), np.dtype(int), np.dtype('datetime64[ns]'))
    if is_df:
        if not data.dtypes.isin(types).all():
            raise TypeError(err_message)
    else:
        if data.dtypes not in types:
            raise TypeError(err_message)
    return


def check_uniqueness(
        data: Union[pd.DataFrame, pd.Series],
        counts: bool = False
) -> Union[pd.Series, bool, int]:
    """Checks if data contains columns with duplicates.

    Args:
        data: Data to be checked for duplicates.
        counts: If True, returns counts of duplicates, if False, returns boolean indicators of duplicates.

    Returns: TODO
        Series with index of column names and values of duplicate counts if `counts` is True, or
        bools indicating presence of duplicates if `counts` is False.
    """
    validate_dtype(data)
    is_df = utils.check_if_df(data)
    if is_df:
        dupes = data.nunique(axis=0).subtract(data.shape[0]).multiply(-1)
        if not counts:
            dupes = dupes.astype(bool)
    else:
        dupes = data.shape[0] - data.nunique()
        if not counts:
            dupes = bool(dupes)
    return dupes
