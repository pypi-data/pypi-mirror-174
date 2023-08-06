import numpy as np
import pandas as pd
from .types import DifferenceCalculation as DifferenceCalculation, Disparity as Disparity, DisparityCalculation as DisparityCalculation, RatioCalculation as RatioCalculation, StatSigTest as StatSigTest
from solas_disparity import const as const, statistical_significance as statistical_significance
from solas_disparity.conditioning import condition as condition
from solas_disparity.utils import pgrg_ordered as pgrg_ordered
from solas_disparity.validation import validation as validation
from typing import Callable, Dict, List, Optional, Union

def custom_disparity_metric(group_data: pd.DataFrame, protected_groups: List[str], reference_groups: List[str], group_categories: List[str], outcome: Union[pd.Series, np.ndarray, pd.DataFrame], metric_requested: Callable, metric_requested_name: Optional[str] = ..., metric_requested_kwargs: Optional[Dict] = ..., label: Optional[Union[pd.Series, np.ndarray, pd.DataFrame]] = ..., sample_weight: Optional[Union[pd.Series, np.ndarray, pd.DataFrame]] = ..., ratio_calculation: RatioCalculation = ..., ratio_threshold: Optional[str] = ..., difference_calculation: DifferenceCalculation = ..., difference_threshold: Optional[str] = ..., statistical_significance_test: Optional[StatSigTest] = ..., statistical_significance_pvalue_threshold: Optional[float] = ..., statistical_significance_kwargs: Optional[Dict] = ...) -> Disparity: ...
