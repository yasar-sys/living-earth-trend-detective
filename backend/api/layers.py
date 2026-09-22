from typing import List

from fastapi import APIRouter, HTTPException

from models.schemas import DataLayer, GlobeLayerData, LayerMetadata
from services.data_loader import get_data_loader

router = APIRouter()


@router.get("/layers", response_model=List[LayerMetadata])
def list_layers():
    return get_data_loader().get_all_meta()


@router.get("/layers/{layer}", response_model=LayerMetadata)
def layer_meta(layer: DataLayer):
    meta = get_data_loader().get_layer_meta(layer)
    if not meta:
        raise HTTPException(404, "Layer not found")
    return meta


@router.get("/layers/{layer}/years", response_model=List[int])
def layer_years(layer: DataLayer):
    years = get_data_loader().get_years(layer)
    if not years:
        raise HTTPException(404, "Layer not found")
    return years


@router.get("/layers/{layer}/data/{year}", response_model=GlobeLayerData)
def layer_data(layer: DataLayer, year: int):
    data = get_data_loader().get_layer_data(layer, year)
    if not data:
        raise HTTPException(404, f"No data for year {year}")
    return data


@router.get("/layers/{layer}/regions")
def layer_regions(layer: DataLayer):
    """id/name/coordinates for every region in this layer (for globe markers)."""
    regions = get_data_loader().get_regions_summary(layer)
    if not regions:
        raise HTTPException(404, "Layer not found")
    return regions
