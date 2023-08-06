from plotly.graph_objects import Figure as Figure
from solas_disparity import const as const
from solas_disparity.const import COLORS as COLORS, SEG_WIDTH_MAX as SEG_WIDTH_MAX
from solas_disparity.types import AdverseImpactRatioByQuantileColumnType as AdverseImpactRatioByQuantileColumnType, AdverseImpactRatioColumnType as AdverseImpactRatioColumnType, CategoricalAdverseImpactRatioColumnType as CategoricalAdverseImpactRatioColumnType, DisparityCalculation as DisparityCalculation, FalseDiscoveryRateColumnType as FalseDiscoveryRateColumnType, FalseNegativeRateColumnType as FalseNegativeRateColumnType, FalsePositiveRateColumnType as FalsePositiveRateColumnType, OddsRatioColumnType as OddsRatioColumnType, PositivePredictiveValueColumnType as PositivePredictiveValueColumnType, ResidualStandardizedMeanDifferenceColumnType as ResidualStandardizedMeanDifferenceColumnType, SegmentedAdverseImpactRatioColumnType as SegmentedAdverseImpactRatioColumnType, StandardizedMeanDifferenceColumnType as StandardizedMeanDifferenceColumnType, TrueNegativeRateColumnType as TrueNegativeRateColumnType, TruePositiveRateColumnType as TruePositiveRateColumnType
from solas_disparity.ui import AUTO_FORMATTERS as AUTO_FORMATTERS
from typing import Dict, Optional

def plot_formatter() -> Dict: ...

class plot:
    def __init__(self, disp) -> None: ...
    def __call__(self, column: Optional[str] = ..., group: Optional[str] = ..., condense: Optional[bool] = ..., top_n_segments: Optional[int] = ...) -> Figure: ...
