"""Data exploration tools."""

__version__ = '0.0.0'


# Binary feature checks
from surveyor._binary_features import check_all_same, check_mostly_same, check_outside_range
# Categorical feature checks
from surveyor._categorical_features import check_mostly_same, check_n_categories
# General feature checks
from surveyor._general_features import check_fuzzy_nulls, check_nulls
# Unique feature checks
from surveyor._unique_features import check_uniqueness


__all__ = [_binary_features, _categorical_features, _general_features, _unique_features]
