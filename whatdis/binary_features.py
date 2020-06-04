# standard library imports
from typing import Union
# third party imports
import numpy as np
import pandas as pd
# local imports
from whatdis import utils


def validate_binary_dtype(data: Union[pd.DataFrame, pd.Series]) -> None:
    """Validates if binary data contains only dtype bool or int.

    Args:
        data: Binary data to be type validated.

    Returns:
        None

    Raises:
        TypeError: If `data` contains dtype other than bool or int
    """
    is_df = utils.check_if_df(data)
    err_message = 'Binary feature columns should be of type bool or int64.'
    if is_df:
        if not data.dtypes.isin((np.dtype(bool), np.dtype(int))).all():
            raise TypeError(err_message)
    else:
        if data.dtypes not in (np.dtype(bool), np.dtype(int)):
            raise TypeError(err_message)
    return


def check_all_same(data: Union[pd.DataFrame, pd.Series]) -> Union[pd.Series, bool]:
    """Checks if binary data contains columns where all values are the same.

    Args:
        data: Binary data to be checked if all values are the same.

    Returns:
        If `data` is a DataFrame, returns a Series with index of column names and values of bools
        indicating if all values are the same. If `data` is a Series, returns a bool indicating
        if all values are the same.
    """
    is_df = utils.check_if_df(data)
    validate_binary_dtype(data)
    if is_df:
        return data.min(axis=0).eq(data.max(axis=0))
    else:
        return data.min() == data.max()


def check_mostly_same(
        data: Union[pd.DataFrame, pd.Series],
        thresh: float = 0.95,
) -> Union[pd.Series, bool]:
    """Checks if binary data contains columns where almost all values are the same.

    Args:
        data: Binary data to be checked if almost all values are the same.
        thresh: Threshold for what proportion of data must be the same to fail check.

    Returns:
        Series with index of column names and values of bools indicating if almost all values are the same.

        If `data` is a DataFrame, returns a Series with index of column names and values of bools
        indicating if almost all values are the same. If `data` is a Series, returns a bool
        indicating if almost all values are the same.

    Raises:
        ValueError: If `thresh` less than or equal to 0.0 or greater than or equal to 1.0.
    """
    if thresh >= 1.0 or thresh <= 0.0:
        raise ValueError('The thresh parameter must be greater than 0.0 and less than 1.0.')
    is_df = utils.check_if_df(data)
    validate_binary_dtype(data)
    if is_df:
        means = data.mean(axis=0)
        return (means >= thresh) | (means <= 1 - thresh)
    else:
        mean = data.mean()
        return mean >= thresh or mean <= 1 - thresh


def check_range(data: Union[pd.DataFrame, pd.Series]) -> Union[pd.Series, bool]:
    """Checks if binary data contains columns where min is less than 0 or max is greater than 1.
    
    Args:
        data: Binary data to be checked if all values are less than 0 or greater than 1.

    Returns:
        If `data` is a DataFrame, returns a Series with index of column names and values of bools
        indicating if the min or max values out of range. If `data` is a Series, returns a bool
        indicating min or max values are out of range.
    """
    is_df = utils.check_if_df(data)
    validate_binary_dtype(data)
    if is_df:
        return (data.min(axis=0) < 0) | (data.max(axis=0) > 1)
    else:
        return data.min() < 0 or data.max() > 1
