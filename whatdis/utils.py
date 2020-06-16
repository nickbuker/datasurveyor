# TODO docstrings
# standard library imports
from typing import Any, Union
# third party imports
import pandas as pd


def check_if_df(data: Any) -> bool:
    """

    Args:
        data:

    Returns:

    """
    if isinstance(data, pd.DataFrame):
        return True
    if isinstance(data, pd.Series):
        return False
    else:
        raise TypeError('Input data must be of type pandas DataFrame or pandas Series.')


def result_to_df(
        data: Union[pd.Series, bool, float, int],
        title: str,
        **kwargs,
) -> pd.DataFrame:
    """

    Args:
        data:
        title:
        **kwargs:

    Returns:

    """
    if isinstance(data, pd.Series):
        d = {'column': data.index, title: data.values}
    else:
        d = {title: (data,)}
        if kwargs:
            kwargs = {k: (v,) for k, v in kwargs.items()}
    d.update(kwargs)
    return pd.DataFrame.from_dict(d).reset_index(drop=True)


def validate_thresh(thresh: float) -> None:
    """

    Args:
        thresh:

    Returns:

    """
    if thresh >= 1.0 or thresh <= 0.0:
        raise ValueError('The thresh parameter must be greater than 0.0 and less than 1.0.')
    return
