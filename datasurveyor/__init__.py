"""Data exploration tools."""

__version__ = '0.0.0'


# Binary feature checks
from datasurveyor._binary_features import BinaryFeatures
# Categorical feature checks
from datasurveyor._categorical_features import CategoricalFeatures
# General feature checks
from datasurveyor._general_features import GeneralFeatures
# Unique feature checks
from datasurveyor._unique_features import UniqueFeatures


__all__ = [_binary_features, _categorical_features, _general_features, _unique_features]
