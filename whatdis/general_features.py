# TODO: update docstrings
# standard library imports
from typing import List, Optional, Union
# third party imports
import pandas as pd
# local imports
from whatdis import utils


def check_nulls(data: Union[pd.DataFrame, pd.Series]) -> pd.DataFrame:
    """Checks if data contains columns with nulls.

    Args:
        data: Data to be checked for nulls.

    Returns:
        Series with index of column names and values null counts if `counts` is True, or bools indicating
        presence of nulls if `counts` is False.
    """
    is_df = utils.check_if_df(data)
    is_nulls = data.isna().any(axis=0)
    count_nulls = data.isna().sum(axis=0)
    if is_df:
        prop_nulls = count_nulls.divide(data.shape[0])
    else:
        prop_nulls = count_nulls / data.shape[0]
    result = utils.result_to_df(
        data=is_nulls,
        title='nulls_present',
        null_count=count_nulls,
        prop_null=prop_nulls
    )
    return result


def check_fuzzy_nulls(
        data: Union[pd.DataFrame, pd.Series],
        add_fuzzy_nulls: Optional[List] = None,
) -> pd.DataFrame:
    """Checks if DataFrame contains columns with fuzzy nulls.

    Args:
        data: Data to be checked for fuzzy nulls.
        add_fuzzy_nulls: Additional items to check as fuzzy nulls.

    Returns:
        Series with index of column names and values fuzzy null counts if `counts` is True, or bools
        indicating presence of fuzzy nulls if `counts` is False.
    """
    is_df = utils.check_if_df(data)
    fuzzy_nulls = ['null', 'Null', 'NULL', '', ' ']
    if add_fuzzy_nulls is not None:
        fuzzy_nulls.extend(add_fuzzy_nulls)
    is_fuzzy_nulls = data.isin(fuzzy_nulls).any(axis=0)
    count_fuzzy_nulls = data.isin(fuzzy_nulls).sum(axis=0)
    if is_df:
        prop_fuzzy_nulls = count_fuzzy_nulls.divide(data.shape[0])
    else:
        prop_fuzzy_nulls = count_fuzzy_nulls / data.shape[0]
    result = utils.result_to_df(
        data=is_fuzzy_nulls,
        title='fuzzy_nulls_present',
        fuzzy_null_count=count_fuzzy_nulls,
        prop_fuzzy_null=prop_fuzzy_nulls,
    )
    return result


if __name__ == '__main__':
    good = pd.DataFrame.from_dict({
        'g1': (True, False, True, False),
        'g2': (0, 1, 0, 1),
        'g3': (False, True, False, True),
    })

    print(check_fuzzy_nulls(good['g1']))