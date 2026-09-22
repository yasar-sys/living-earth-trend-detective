from typing import List

from fastapi import APIRouter, HTTPException

from models.schemas import DataLayer, RegionData, TrendResult
from services.data_loader import get_data_loader
from services.trend_analysis import TrendAnalyzer

router = APIRouter()


@router.get("/layers/{layer}/regions/{region_id}", response_model=RegionData)
def region_series(layer: DataLayer, region_id: str):
    data = get_data_loader().get_region_series(layer, region_id)
    if not data:
        raise HTTPException(404, "Region not found")
    return data


@router.get("/layers/{layer}/regions/{region_id}/trend", response_model=TrendResult)
def region_trend(layer: DataLayer, region_id: str):
    loader = get_data_loader()
    data = loader.get_region_series(layer, region_id)
    if not data:
        raise HTTPException(404, "Region not found")

    trend = TrendAnalyzer.calculate_trend(
        data.time_series, data.region_id, data.region_name, layer
    )
    if not trend:
        raise HTTPException(400, "Insufficient data for trend analysis")
    return trend


@router.get("/layers/{layer}/trends", response_model=List[TrendResult])
def all_trends(layer: DataLayer):
    loader = get_data_loader()
    regions = loader.get_raw_regions(layer)
    if not regions:
        raise HTTPException(404, "Layer not found")
    return TrendAnalyzer.calculate_trends_batch(regions, layer)
