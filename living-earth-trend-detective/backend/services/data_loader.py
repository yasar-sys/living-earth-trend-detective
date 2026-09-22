import json
import os
from pathlib import Path
from typing import Dict, List, Optional

from cachetools import TTLCache

from models.schemas import (
    DataLayer,
    DataSourceInfo,
    GlobeLayerData,
    LayerMetadata,
    RegionData,
    RegionType,
    TimeSeriesPoint,
)

# --- Optional Cloudflare R2 / S3 config -------------------------------
# If these env vars are unset, the loader silently falls back to the
# JSON files bundled in backend/data/ (no external storage required).
R2_ENDPOINT = os.getenv("R2_ENDPOINT_URL")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET = os.getenv("R2_BUCKET_NAME", "living-earth-data")
R2_PREFIX = os.getenv("R2_PREFIX", "v1/")

LOCAL_DATA_DIR = Path(__file__).resolve().parent.parent / "data"

_s3_client = None


def _get_s3_client():
    global _s3_client
    if _s3_client is None and all([R2_ENDPOINT, R2_ACCESS_KEY, R2_SECRET_KEY]):
        import boto3
        from botocore.config import Config as BotoConfig

        _s3_client = boto3.client(
            "s3",
            endpoint_url=R2_ENDPOINT,
            aws_access_key_id=R2_ACCESS_KEY,
            aws_secret_access_key=R2_SECRET_KEY,
            config=BotoConfig(connect_timeout=5, read_timeout=10, retries={"max_attempts": 2}),
        )
    return _s3_client


class DataLoader:
    def __init__(self) -> None:
        self._cache = TTLCache(maxsize=20, ttl=3600)
        self._region_meta: Dict[str, dict] = {}
        self._layer_meta: Dict[DataLayer, LayerMetadata] = {}
        self._load_all()

    def _fetch_json(self, layer: DataLayer) -> Optional[dict]:
        filename = f"{layer.value}.json"

        client = _get_s3_client()
        if client:
            try:
                obj = client.get_object(Bucket=R2_BUCKET, Key=f"{R2_PREFIX}{filename}")
                return json.loads(obj["Body"].read())
            except Exception as exc:  # noqa: BLE001
                print(f"[DataLoader] R2 fetch failed for {filename}: {exc}")

        local_path = LOCAL_DATA_DIR / filename
        if local_path.exists():
            with open(local_path, "r", encoding="utf-8") as f:
                return json.load(f)

        print(f"[DataLoader] WARNING: no data found for {filename}")
        return None

    def _load_all(self) -> None:
        for layer in DataLayer:
            data = self._fetch_json(layer)
            if not data:
                continue
            self._cache[f"layer_{layer.value}"] = data
            self._build_meta(layer, data)

    def _build_meta(self, layer: DataLayer, data: dict) -> None:
        sources = [DataSourceInfo(**s) for s in data.get("sources", [])]
        years = set()

        for region_id, region in data.get("regions", {}).items():
            for point in region.get("time_series", []):
                years.add(point["year"])
            if region_id not in self._region_meta:
                self._region_meta[region_id] = {
                    "region_name": region.get("name", region_id),
                    "region_type": region.get("type", "custom"),
                    "coordinates": region.get("coordinates", [0, 0]),
                }

        self._layer_meta[layer] = LayerMetadata(
            layer=layer,
            display_name=data.get("display_name", layer.value),
            description=data.get("description", ""),
            unit=data.get("unit", ""),
            sources=sources,
            available_years=sorted(years),
            regions=list(data.get("regions", {}).keys()),
        )

    @staticmethod
    def _color_scale(layer: DataLayer) -> List[str]:
        scales = {
            DataLayer.TEMPERATURE: [
                "#2166AC", "#67A9CF", "#D1E5F0", "#F7F7F7", "#FDDBC7", "#EF8A62", "#B2182B",
            ],
            DataLayer.SEA_ICE: [
                "#08306B", "#08519C", "#2171B5", "#4292C6", "#6BAED6", "#9ECAE1", "#C6DBEF",
            ],
            DataLayer.CO2: [
                "#1A9850", "#66BD63", "#A6D96A", "#D9EF8B", "#FFFFBF", "#FEE08B", "#FDAE61", "#D73027",
            ],
        }
        return scales.get(layer, ["#6B7280", "#F2A93B"])

    # --- Public API ----------------------------------------------------

    def get_layer_data(self, layer: DataLayer, year: int) -> Optional[GlobeLayerData]:
        data = self._cache.get(f"layer_{layer.value}")
        if not data:
            return None

        year_values: Dict[str, float] = {}
        values: List[float] = []
        for region_id, region in data.get("regions", {}).items():
            for point in region.get("time_series", []):
                if point["year"] == year:
                    year_values[region_id] = point["value"]
                    values.append(point["value"])
                    break

        if not values:
            return None

        meta = self._layer_meta.get(layer)
        return GlobeLayerData(
            layer=layer,
            year=year,
            data=year_values,
            min_value=min(values),
            max_value=max(values),
            unit=meta.unit if meta else "",
            color_scale=self._color_scale(layer),
        )

    def get_region_series(self, layer: DataLayer, region_id: str) -> Optional[RegionData]:
        data = self._cache.get(f"layer_{layer.value}")
        if not data:
            return None
        region = data.get("regions", {}).get(region_id)
        if not region:
            return None

        meta = self._region_meta.get(region_id, {})
        return RegionData(
            region_id=region_id,
            region_name=meta.get("region_name", region_id),
            region_type=RegionType(meta.get("region_type", "custom")),
            coordinates=meta.get("coordinates", [0, 0]),
            time_series=[TimeSeriesPoint(**p) for p in region.get("time_series", [])],
            metadata=region.get("metadata", {}),
        )

    def get_layer_meta(self, layer: DataLayer) -> Optional[LayerMetadata]:
        return self._layer_meta.get(layer)

    def get_all_meta(self) -> List[LayerMetadata]:
        return list(self._layer_meta.values())

    def get_years(self, layer: DataLayer) -> List[int]:
        meta = self._layer_meta.get(layer)
        return meta.available_years if meta else []

    def get_raw_regions(self, layer: DataLayer) -> dict:
        data = self._cache.get(f"layer_{layer.value}")
        return data.get("regions", {}) if data else {}

    def get_regions_summary(self, layer: DataLayer) -> List[dict]:
        """Lightweight id/name/coordinates list, used to place markers on the globe."""
        data = self._cache.get(f"layer_{layer.value}")
        if not data:
            return []
        out = []
        for region_id, region in data.get("regions", {}).items():
            out.append(
                {
                    "region_id": region_id,
                    "region_name": region.get("name", region_id),
                    "coordinates": region.get("coordinates", [0, 0]),
                }
            )
        return out


# --- Singleton (persists across warm serverless invocations) ----------
_loader: Optional[DataLoader] = None


def get_data_loader() -> DataLoader:
    global _loader
    if _loader is None:
        _loader = DataLoader()
    return _loader
