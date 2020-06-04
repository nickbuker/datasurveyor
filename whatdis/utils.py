# standard library imports
from typing import Any
# third party imports
import pandas as pd


def check_if_df(data: Any) -> bool:
    if isinstance(data, pd.DataFrame):
        return True
    if isinstance(data, pd.Series):
        return False
    else:
        raise TypeError('Input data must be of type pandas DataFrame or pandas Series.')
