# TODO: docstrings
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
) -> pd.DataFrame:
    """Checks if data contains columns with duplicates.

    Args:
        data: Data to be checked for duplicates.

    Returns: TODO
        Series with index of column names and values of duplicate counts if `counts` is True, or
        bools indicating presence of duplicates if `counts` is False.
    """
    # TODO: add null detection
    validate_dtype(data)
    is_df = utils.check_if_df(data)
    if is_df:
        count_dupes = data.nunique(axis=0).subtract(data.shape[0]).multiply(-1)
        is_dupes = count_dupes.astype(bool)
        prop_dupes = count_dupes.divide(data.shape[0])
    else:
        count_dupes = data.shape[0] - data.nunique()
        is_dupes = bool(count_dupes)
        prop_dupes = count_dupes / data.shape[0]
    result = utils.result_to_df(
        data=is_dupes,
        title='dupes_present',
        dupe_count=count_dupes,
        prop_dupe=prop_dupes
    )
    return result
