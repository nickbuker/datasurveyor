# standard library imports
from typing import Union
# third party imports
import numpy as np
import pandas as pd
# local imports
from datasurveyor import _utils


class UniqueFeatures:

    @staticmethod
    def _validate_unique_dtype(data: Union[pd.DataFrame, pd.Series]) -> None:
        """Validates that unique data contains only dtype object, int, or datetime.

        Args:
            data: Unique data to be validated.

        Returns:
            None

        Raises:
            TypeError: If `data` contains dtype other than object, int, or datetime.
        """
        is_df = _utils.check_if_df(data)
        err_message = 'Unique feature columns should be of type object, int64, or datetime64.'
        types = (np.dtype('O'), np.dtype(int), np.dtype('datetime64[ns]'))
        if is_df:
            if not data.dtypes.isin(types).all():
                raise TypeError(err_message)
        else:
            if data.dtypes not in types:
                raise TypeError(err_message)
        return

    @staticmethod
    def check_uniqueness(
            data: Union[pd.DataFrame, pd.Series],
    ) -> pd.DataFrame:
        """Checks if unique data contains columns with duplicates.

        Args:
            data: Data to be checked for duplicates.

        Returns:
            DataFrame with bool(s) indicating if data contains duplicates, the count of
            duplicates present, and the proportion of duplicates.

        Raises:
            ValueError: If unique data contains nulls.
        """
        UniqueFeatures._validate_unique_dtype(data)
        is_df = _utils.check_if_df(data)
        err_message = 'Columns with unique data should not contain nulls.'
        if is_df:
            if data.isna().any(axis=None):
                raise ValueError(err_message)
            count_dupes = data.nunique(axis=0).subtract(data.shape[0]).multiply(-1)
            is_dupes = count_dupes.astype(bool)
            prop_dupes = count_dupes.divide(data.shape[0])
        else:
            if data.isna().any():
                raise ValueError(err_message)
            count_dupes = data.shape[0] - data.nunique()
            is_dupes = bool(count_dupes)
            prop_dupes = count_dupes / data.shape[0]
        result = _utils.result_to_df(
            data=is_dupes,
            title='dupes_present',
            dupe_count=count_dupes,
            prop_dupe=prop_dupes
        )
        return result
