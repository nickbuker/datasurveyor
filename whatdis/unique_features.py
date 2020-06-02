# third party imports
import pandas as pd


def type_check():
    # TODO: add type check for bools, floats, datetime, etc.
    pass


def check_uniqueness(df: pd.DataFrame, counts: bool = False) -> pd.Series:
    """ TODO

    Args:
        df:
        counts:

    Returns:

    """
    # TODO add type check and null check
    dupes = df.nunique(axis=0).subtract(df.shape[0]).multiply(-1)
    if not counts:
        dupes = dupes.astype(bool)
    return dupes
