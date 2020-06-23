# standard library imports
from typing import Any, Union
# third party imports
import pandas as pd


def check_if_df(data: Any) -> bool:
    """Checks type of data and raises error if not Pandas DataFrame or Series.

    Args:
        data: Data to be type checked.
    Returns:
        True if `data` is of type Pandas DataFrame.
        False if `data` is of type Pandas Series.

    Raises:
        TypeError if  `data` is not of type pandas DataFrame or Series.
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
    """Generates an output DataFrame with tidy formatting.

    Args:
        data: Base data to be included in DataFrame.
        title: Name of test being run (used as a column name in output DataFrame).
        **kwargs: Additional data to be included in the output DataFrame where:
        argument name = output column name and argument value = output column value.

    Returns:
        Output data as a DataFrame.
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
    """Validates the proportion provided.

    Args:
        thresh: Proportion to be validated.

    Returns:
        None

    Raises:
        ValueError if `thresh` is not between 0.0 and 1.0 (inclusive).
    """
    if thresh >= 1.0 or thresh <= 0.0:
        raise ValueError('The thresh parameter must be greater than 0.0 and less than 1.0.')
    return
