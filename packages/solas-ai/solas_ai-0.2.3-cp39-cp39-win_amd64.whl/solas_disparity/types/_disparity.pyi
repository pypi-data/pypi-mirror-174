import pandas as pd
from ._adverse_impact_ratio_by_quantile_column_type import AdverseImpactRatioByQuantileColumnType as AdverseImpactRatioByQuantileColumnType
from ._adverse_impact_ratio_column_type import AdverseImpactRatioColumnType as AdverseImpactRatioColumnType
from ._disparity_calculation import DisparityCalculation as DisparityCalculation
from ._false_discovery_rate_column_type import FalseDiscoveryRateColumnType as FalseDiscoveryRateColumnType
from ._false_negative_rate_column_type import FalseNegativeRateColumnType as FalseNegativeRateColumnType
from ._false_positive_rate_column_type import FalsePositiveRateColumnType as FalsePositiveRateColumnType
from ._odds_ratio_column_type import OddsRatioColumnType as OddsRatioColumnType
from ._positive_predictive_value_column_type import PositivePredictiveValueColumnType as PositivePredictiveValueColumnType
from ._residual_smd_denominator import ResidualSMDDenominator as ResidualSMDDenominator
from ._residual_standardized_mean_difference_column_type import ResidualStandardizedMeanDifferenceColumnType as ResidualStandardizedMeanDifferenceColumnType
from ._segmented_adverse_impact_ratio_column_type import SegmentedAdverseImpactRatioColumnType as SegmentedAdverseImpactRatioColumnType
from ._shortfall_method import ShortfallMethod as ShortfallMethod
from ._smd_denominator import SMDDenominator as SMDDenominator
from ._standardized_mean_difference_column_type import StandardizedMeanDifferenceColumnType as StandardizedMeanDifferenceColumnType
from ._stat_sig import StatSig as StatSig
from ._stat_sig_hypothesis import StatSigHypothesis as StatSigHypothesis
from ._stat_sig_test import StatSigTest as StatSigTest
from ._true_negative_rate_column_type import TrueNegativeRateColumnType as TrueNegativeRateColumnType
from ._true_positive_rate_column_type import TruePositiveRateColumnType as TruePositiveRateColumnType
from pathlib import Path
from solas_disparity import const as const, ui as ui
from typing import Callable, Dict, List, Optional, Union

class Disparity:
    @property
    def plot(self): ...
    @plot.setter
    def plot(self, value) -> None: ...
    disparity_type: DisparityCalculation
    summary_table: pd.DataFrame
    protected_groups: List[str]
    reference_groups: List[str]
    group_categories: List[str]
    statistical_significance: StatSig
    stat_sig_test: Optional[Union[str, StatSigTest]]
    stat_sig_p_values: Optional[pd.Series]
    stat_sig_summary_table: Optional[pd.DataFrame]
    stat_sig_t_statistics: Optional[pd.DataFrame]
    stat_sig_standard_errors: Optional[pd.DataFrame]
    stat_sig_z_scores: Optional[pd.DataFrame]
    smd_threshold: Optional[float]
    residual_smd_threshold: Optional[float]
    smd_denominator: Optional[str]
    residual_smd_denominator: Optional[str]
    lower_score_favorable: Optional[bool]
    odds_ratio_threshold: Optional[float]
    air_threshold: Optional[float]
    percent_difference_threshold: Optional[float]
    max_for_fishers: Optional[int]
    alternative_hypothesis: Optional[Union[str, StatSigHypothesis]]
    shortfall_method: Optional[Union[str, ShortfallMethod]]
    quantile_summaries: Optional[List[pd.DataFrame]]
    category_summaries: Optional[List[pd.DataFrame]]
    summary_table_hstacked: Optional[pd.DataFrame]
    quantile_air_results: Optional[List[Disparity]]
    categorical_air_results: Optional[List[Disparity]]
    quantile_statistical_significance_results: Optional[List[StatSig]]
    category_statistical_significance_results: Optional[List[StatSig]]
    input_quantiles: Optional[List[float]]
    ordinal_categories: Optional[List[float]]
    quantile_cutoffs_table: Optional[pd.DataFrame]
    outcome_category_mapping: Optional[pd.DataFrame]
    segment_air_results: Optional[List[Disparity]]
    segment_summaries: Optional[List[pd.DataFrame]]
    segment_statistical_significance_results: Optional[List[StatSig]]
    segments: Optional[List[Union[int, float, str]]]
    summary_table_across_segments: Optional[pd.DataFrame]
    summary_table_by_segments: Optional[pd.DataFrame]
    fdr_threshold: Optional[float]
    ratio_calculation: Optional[str]
    ratio_threshold: Optional[float]
    difference_calculation: Optional[str]
    difference_threshold: Optional[float]
    metric_requested: Callable
    metric_requested_name: Optional[str]
    metric_requested_kwargs: Optional[Dict]
    statistical_significance_test: Optional[StatSigTest]
    statistical_significance_pvalue_threshold: Optional[float]
    statistical_significance_kwargs: Optional[Dict]
    metric_columns: Optional[List[str]]
    @property
    def affected_groups(self) -> List[str]: ...
    @property
    def affected_groups_by_segment(self) -> Optional[List[str]]: ...
    @property
    def affected_reference_by_segment(self) -> Optional[List[str]]: ...
    @property
    def affected_categories_by_segment(self) -> Optional[List[str]]: ...
    @property
    def affected_reference(self) -> List[str]: ...
    @property
    def affected_categories(self) -> Optional[List[str]]: ...
    def to_csv(self, file_path: Union[str, Path]) -> None: ...
    def to_excel(self, file_path: Union[str, Path]): ...
    def show(self) -> None: ...
    def __rich__(self) -> None: ...
    def to_image(self, file_path: Union[str, Path], column: Union[str, AdverseImpactRatioColumnType, AdverseImpactRatioByQuantileColumnType, SegmentedAdverseImpactRatioColumnType, StandardizedMeanDifferenceColumnType, ResidualStandardizedMeanDifferenceColumnType, OddsRatioColumnType, TruePositiveRateColumnType, FalsePositiveRateColumnType, TrueNegativeRateColumnType, FalseNegativeRateColumnType, PositivePredictiveValueColumnType, FalseDiscoveryRateColumnType], group: Optional[str] = ..., condense: Optional[bool] = ..., top_n_segments: Optional[int] = ...) -> None: ...
    def __init__(self, disparity_type, summary_table, protected_groups, reference_groups, group_categories, statistical_significance, stat_sig_test, stat_sig_p_values, stat_sig_summary_table, stat_sig_t_statistics, stat_sig_standard_errors, stat_sig_z_scores, smd_threshold, residual_smd_threshold, smd_denominator, residual_smd_denominator, lower_score_favorable, odds_ratio_threshold, air_threshold, percent_difference_threshold, max_for_fishers, alternative_hypothesis, shortfall_method, quantile_summaries, category_summaries, summary_table_hstacked, quantile_air_results, categorical_air_results, quantile_statistical_significance_results, category_statistical_significance_results, input_quantiles, ordinal_categories, quantile_cutoffs_table, outcome_category_mapping, segment_air_results, segment_summaries, segment_statistical_significance_results, segments, summary_table_across_segments, summary_table_by_segments, fdr_threshold, ratio_calculation, ratio_threshold, difference_calculation, difference_threshold, metric_requested, metric_requested_name, metric_requested_kwargs, statistical_significance_test, statistical_significance_pvalue_threshold, statistical_significance_kwargs, metric_columns) -> None: ...
    def __lt__(self, other): ...
    def __le__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...
