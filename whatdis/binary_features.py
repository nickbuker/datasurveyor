# third party imports
import numpy as np
import pandas as pd


def validate_dtype(df: pd.DataFrame) -> None:
    if not df.dtypes.isin((np.dtype(bool), np.dtype(int))).all():
        raise TypeError('Binary feature columns should be of type bool or int64.')
    return


def check_all_same(df: pd.DataFrame) -> pd.Series:
    validate_dtype(df)
    return df.min(axis=0).eq(df.max(axis=0))


def check_mostly_same(df: pd.DataFrame, thresh: float = 0.95) -> pd.Series:
    if thresh >= 1.0 or thresh <= 0.0:
        raise ValueError('The thresh parameter must be greater than 0.0 and less than 1.0.')
    validate_dtype(df)
    means = df.mean(axis=0)
    return (means >= thresh) | (means <= 1 - thresh)


def check_range(df: pd.DataFrame) -> pd.Series:
    validate_dtype(df)
    return (df.min(axis=0) < 0) | (df.max(axis=0) > 1)
