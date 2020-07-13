# standard library imports
from typing import Union
# third party imports
import numpy as np
import pandas as pd
# local imports
from datasurveyor import _utils


class CategoricalFeatures:

    @staticmethod
    def _validate_categorical_dtype(data: Union[pd.DataFrame, pd.Series]) -> None:
        """Validates that categorical data contains only dtype int or object (str).

        Args:
            data: Categorical data to be type validated.

        Returns:
            None

        Raises:
            TypeError: If `data` contains dtype other than bool or object (str).
        """
        is_df = _utils.check_if_df(data)
        err_message = 'Unique feature columns should be of type object or int64.'
        types = (np.dtype('O'), np.dtype(int))
        if is_df:
            if not data.dtypes.isin(types).all():
                raise TypeError(err_message)
        else:
            if data.dtypes not in types:
                raise TypeError(err_message)
        return

    @staticmethod
    def check_mostly_same(
            data: Union[pd.DataFrame, pd.Series],
            thresh: float = 0.95,
            dropna: bool = False,
    ) -> pd.DataFrame:
        """Checks if categorical data contains almost all the same category.

        Args:
            data: Categorical data to be checked if almost all the same category.
            thresh: Threshold for what proportion of data must be the same category to fail check.
            dropna: If True: ignores nulls, if False: counts nulls as a category.

        Returns:
            DataFrame with bool(s) indicating if data contains almost all the same category, the
            value of threshold used to determine if mostly same, the most common category, the
            count of the most common category, and the proportion of the most common category.
        """
        _utils.validate_thresh(thresh)
        CategoricalFeatures._validate_categorical_dtype(data)
        is_df = _utils.check_if_df(data)
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
        result = _utils.result_to_df(
            mostly_same,
            title='mostly_same',
            thresh=thresh,
            most_common=most_common,
            count=count_common,
            prop=prop_common,
        )
        return result

    @staticmethod
    def check_n_categories(
            data: Union[pd.DataFrame, pd.Series],
            dropna: bool = False,
    ) -> pd.DataFrame:
        """Counts the number of categories.

        Args:
            data: Data to count categories for.
            dropna: If True: ignores nulls, if False: counts nulls as a category.

        Returns:
            DataFrame with count(s) of categories.
        """
        CategoricalFeatures._validate_categorical_dtype(data)
        is_df = _utils.check_if_df(data)
        if is_df:
            result = data.nunique(axis=0, dropna=dropna)
        else:
            result = data.nunique(dropna=dropna)
        return _utils.result_to_df(result, title='n_categories')
