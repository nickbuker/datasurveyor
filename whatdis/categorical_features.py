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


def check_mostly_same(
        data: Union[pd.DataFrame, pd.Series],
        thresh: float = 0.95,
        dropna: bool = False,
) -> pd.DataFrame:
    """TODO

    Args:
        data:
        thresh:
        dropna:

    Returns:

    """
    # TODO: test me!
    utils.validate_thresh(thresh)
    validate_categorical_dtype(data)
    is_df = utils.check_if_df(data)
    if is_df:
        most_common = data.mode(axis=0, dropna=dropna).loc[0, :]
        count_common = data.eq(most_common).sum(axis=0)
        prop_common = count_common.divide(data.shape[0])
        mostly_same = prop_common.ge(thresh)
    else:
        most_common = data.mode()[0]
        count_common = data.eq(most_common).sum()
        prop_common = count_common / data.shape[0]
        mostly_same = prop_common >= thresh
    result = utils.result_to_df(
        mostly_same,
        title='mostly_same',
        thresh=thresh,
        most_common=most_common,
        count=count_common,
        prop=prop_common,
    )
    return result


def check_n_categories(
        data: Union[pd.DataFrame, pd.Series],
        dropna: bool = False,
) -> pd.DataFrame:
    """TODO

    Args:
        data:
        dropna:

    Returns:

    """
    validate_categorical_dtype(data)
    is_df = utils.check_if_df(data)
    if is_df:
        result = data.nunique(axis=0, dropna=dropna)
    else:
        result = data.nunique(dropna=dropna)
    return utils.result_to_df(result, title='n_categories')
