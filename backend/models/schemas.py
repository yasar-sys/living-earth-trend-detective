from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class DataLayer(str, Enum):
    TEMPERATURE = "temperature_anomaly"
    SEA_ICE = "sea_ice_extent"
    CO2 = "co2_concentration"


class RegionType(str, Enum):
    COUNTRY = "country"
    CONTINENT = "continent"
    CUSTOM = "custom"


class Significance(str, Enum):
    SIGNIFICANT = "significant"
    NOT_SIGNIFICANT = "not_significant"
    INSUFFICIENT_DATA = "insufficient_data"


class TimeSeriesPoint(BaseModel):
    year: int
    value: float
    unit: str


class RegionData(BaseModel):
    region_id: str
    region_name: str
    region_type: RegionType
    coordinates: List[float]  # [lat, lon]
    time_series: List[TimeSeriesPoint]
    metadata: Dict[str, Any] = {}


class TrendResult(BaseModel):
    region_id: str
    region_name: str
    layer: DataLayer
    slope_per_decade: float
    p_value: float
    significance: Significance
    tau: float
    sample_size: int
    start_year: int
    end_year: int
    unit: str


class GlobeLayerData(BaseModel):
    layer: DataLayer
    year: int
    data: Dict[str, float]  # region_id -> value
    min_value: float
    max_value: float
    unit: str
    color_scale: List[str]


class DataSourceInfo(BaseModel):
    name: str
    url: str
    citation: str


class LayerMetadata(BaseModel):
    layer: DataLayer
    display_name: str
    description: str
    unit: str
    sources: List[DataSourceInfo]
    available_years: List[int]
    regions: List[str]


class DetectiveCase(BaseModel):
    id: str
    title: str
    layer: DataLayer
    regions: List[str]
    narrative: str
    explanation: str
    key_mechanism: str
    comparison_years: List[int]


class DetectiveQuestion(BaseModel):
    id: str
    layer: DataLayer
    region: str
    question: str
    options: List[str]
    correct_answer: int


class HealthResponse(BaseModel):
    status: str
    layers_loaded: int
