from typing import List, Optional

import numpy as np
import pymannkendall as mk

from models.schemas import DataLayer, Significance, TimeSeriesPoint, TrendResult


class TrendAnalyzer:
    """Mann-Kendall trend test + Sen's slope, per region/layer."""

    @staticmethod
    def calculate_trend(
        time_series: List[TimeSeriesPoint],
        region_id: str,
        region_name: str,
        layer: DataLayer,
        min_samples: int = 8,
    ) -> Optional[TrendResult]:
        if len(time_series) < min_samples:
            return TrendResult(
                region_id=region_id,
                region_name=region_name,
                layer=layer,
                slope_per_decade=0.0,
                p_value=1.0,
                significance=Significance.INSUFFICIENT_DATA,
                tau=0.0,
                sample_size=len(time_series),
                start_year=time_series[0].year if time_series else 0,
                end_year=time_series[-1].year if time_series else 0,
                unit=time_series[0].unit if time_series else "",
            )

        sorted_ts = sorted(time_series, key=lambda p: p.year)
        years = np.array([p.year for p in sorted_ts], dtype=float)
        values = np.array([p.value for p in sorted_ts], dtype=float)
        unit = sorted_ts[0].unit

        try:
            result = mk.original_test(values, alpha=0.05)
            slope_per_decade = float(result.slope) * 10
            significance = (
                Significance.SIGNIFICANT if result.p < 0.05 else Significance.NOT_SIGNIFICANT
            )

            return TrendResult(
                region_id=region_id,
                region_name=region_name,
                layer=layer,
                slope_per_decade=round(slope_per_decade, 4),
                p_value=round(float(result.p), 5),
                significance=significance,
                tau=round(float(result.Tau), 4),
                sample_size=len(values),
                start_year=int(years[0]),
                end_year=int(years[-1]),
                unit=unit,
            )
        except Exception as exc:  # noqa: BLE001
            print(f"[TrendAnalyzer] failed for {region_id}: {exc}")
            return None

    @staticmethod
    def calculate_trends_batch(regions: dict, layer: DataLayer) -> List[TrendResult]:
        results = []
        for region_id, region in regions.items():
            ts = [TimeSeriesPoint(**p) for p in region.get("time_series", [])]
            trend = TrendAnalyzer.calculate_trend(
                ts, region_id, region.get("name", region_id), layer
            )
            if trend:
                results.append(trend)
        return results
