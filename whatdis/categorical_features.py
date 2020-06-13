# standard library imports
from typing import Union
# third party imports
import numpy as np
import pandas as pd
# local imports
from whatdis import utils


def validate_categorical_dtype(data: Union[pd.DataFrame, pd.Series]) -> None:
    """TODO

    Args:
        data:

    Returns:

    """
    is_df = utils.check_if_df(data)
    err_message = 'Unique feature columns should be of type object or int64.'
    types = (np.dtype('O'), np.dtype(int))
    if is_df:
        if not data.dtypes.isin(types).all():
            raise TypeError(err_message)
    else:
        if data.dtypes not in types:
            raise TypeError(err_message)
    return


def check_all_same(
        data: Union[pd.DataFrame, pd.Series],
        dropna: bool = True,
) -> Union[pd.Series, bool]:
    """TODO

    Args:
        data:
        dropna:

    Returns:

    """
    pass


def check_mostly_same(
        data: Union[pd.DataFrame, pd.Series],
        dropna: bool = True,
) -> Union[pd.Series, bool]:
    """TODO

    Args:
        data:
        dropna:

    Returns:

    """
    pass


def check_n_categories(
        data: Union[pd.DataFrame, pd.Series],
        dropna: bool = True,
) -> Union[pd.Series, int]:
    """TODO

    Args:
        data:
        dropna:

    Returns:

    """
    validate_categorical_dtype(data)
    is_df = utils.check_if_df(data)
    if is_df:
        return data.nunique(axis=0, dropna=dropna)
    else:
        return data.nunique(dropna=dropna)
