# standard library imports
from typing import Union
# third party imports
import numpy as np
import pandas as pd
# local imports
from datasurveyor import _utils


class BinaryFeatures:

    @staticmethod
    def _validate_binary_dtype(data: Union[pd.DataFrame, pd.Series]) -> None:
        """Validates that binary data contains only dtype bool or int.

        Args:
            data: Binary data to be type validated.

        Returns:
            None

        Raises:
            TypeError: If `data` contains dtype other than bool or int.
        """
        is_df = _utils.check_if_df(data)
        err_message = 'Binary feature columns should be of type bool or int64.'
        types = (np.dtype(bool), np.dtype(int))
        if is_df:
            if not data.dtypes.isin(types).all():
                raise TypeError(err_message)
        else:
            if data.dtypes not in types:
                raise TypeError(err_message)
        return

    @staticmethod
    def check_all_same(data: Union[pd.DataFrame, pd.Series]) -> Union[pd.DataFrame]:
        """Checks if binary data contains all the same value.

        Args:
            data: Binary data to be checked if all values are the same.

        Returns:
            DataFrame with bool(s) indicating if data contains all the same value.
        """
        is_df = _utils.check_if_df(data)
        BinaryFeatures._validate_binary_dtype(data)
        if is_df:
            result = data.min(axis=0).eq(data.max(axis=0))
        else:
            result = data.min() == data.max()
        return _utils.result_to_df(result, title='all_same')

    @staticmethod
    def check_mostly_same(
            data: Union[pd.DataFrame, pd.Series],
            thresh: float = 0.95,
    ) -> pd.DataFrame:
        """Checks if binary data contains almost all the same value.

        Args:
            data: Binary data to be checked if almost all values are the same.
            thresh: Threshold for what proportion of data must be the same to fail check.

        Returns:
            DataFrame with bool(s) indicating if data contains all the same value, the
            value of threshold used to determine if mostly same, and the average value(s).

        Raises:
            ValueError: If `thresh` less than or equal to 0.0 or greater than or equal to 1.0.
        """
        _utils.validate_thresh(thresh)
        is_df = _utils.check_if_df(data)
        BinaryFeatures._validate_binary_dtype(data)
        if is_df:
            mean = data.mean(axis=0)
            result = (mean >= thresh) | (mean <= 1 - thresh)
        else:
            mean = data.mean()
            result = mean >= thresh or mean <= 1 - thresh
        return _utils.result_to_df(data=result, title='mostly_same', thresh=thresh, mean=mean)

    @staticmethod
    def check_outside_range(data: Union[pd.DataFrame, pd.Series]) -> pd.DataFrame:
        """Checks if binary data contains columns where min is less than 0 or max is greater than 1.

        Args:
            data: Binary data to be checked if any values are less than 0 or greater than 1.

        Returns:
            DataFrame with bool(s) indicating if data contains any values outside of the expected range.
        """
        is_df = _utils.check_if_df(data)
        BinaryFeatures._validate_binary_dtype(data)
        if is_df:
            result = (data.min(axis=0) < 0) | (data.max(axis=0) > 1)
        else:
            result = data.min() < 0 or data.max() > 1
        return _utils.result_to_df(data=result, title='outside_range')
