"""
Generates PLACEHOLDER datasets, anchored to a few verified real published
figures so the demo is realistic, but still not the full official record.

Verified real anchor points used (via NASA/NOAA public statements, Sept 2026):
  - Global temperature anomaly, 2024, vs 1951-1980 baseline: 1.28 degC
    (NASA GISS / science.nasa.gov earth-indicators page)
  - Global mean CO2, 2024 (NOAA GML annual analysis): 422.8 ppm
  - 1980 anchors (widely published GISTEMP/Mauna Loa figures): ~0.26 degC
    anomaly, ~338.7 ppm CO2

IMPORTANT: everything BETWEEN those anchor points, and every region other
than "global", is still interpolated/synthetic — not the real year-by-year
record. Every file is tagged "is_placeholder": true. For the real, full
historical series, run backend/scripts/fetch_real_data.py on a machine with
normal internet access (see DATA_PIPELINE.md) and replace these files.

Run:  python backend/scripts/generate_dummy_data.py
"""
import json
import random
from pathlib import Path

random.seed(42)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

YEARS = list(range(1980, 2025))

# Real anchors (see module docstring)
TEMP_1980, TEMP_2024 = 0.26, 1.28          # degC, global, vs 1951-1980
CO2_1980, CO2_2024 = 338.7, 422.8          # ppm, global mean


def interp(v0: float, v1: float, year: int, y0: int = 1980, y1: int = 2024) -> float:
    """Linear interpolation between two real anchor points."""
    t = (year - y0) / (y1 - y0)
    return v0 + t * (v1 - v0)


def noisy(base: float, trend_per_year: float, year: int, start_year: int, noise: float) -> float:
    value = base + trend_per_year * (year - start_year)
    return round(value + random.uniform(-noise, noise), 3)


def region(name: str, r_type: str, coords: list[float]) -> dict:
    return {"name": name, "type": r_type, "coordinates": coords}


# ---------------------------------------------------------------------
# Temperature Anomaly (°C, vs 1951-1980 baseline)
# "global" is anchored to real 1980/2024 published values; other regions
# apply a plausible amplification ratio on top of that real global curve
# (land warms faster than ocean, poles amplify further) - the ratios are
# illustrative, not measured, hence still "is_placeholder": true.
# ---------------------------------------------------------------------
temp_regions = {
    "global": {**region("Global", "custom", [0, 0]), "ratio": 1.00, "offset": 0.0, "noise": 0.05},
    "global_land": {**region("Global Land", "custom", [0, 0]), "ratio": 1.55, "offset": -0.05, "noise": 0.08},
    "global_ocean": {**region("Global Ocean", "custom", [0, 0]), "ratio": 0.70, "offset": 0.05, "noise": 0.04},
    "arctic": {**region("Arctic", "custom", [75, 0]), "ratio": 2.70, "offset": -0.10, "noise": 0.15},
    "antarctic": {**region("Antarctic", "custom", [-75, 0]), "ratio": 0.80, "offset": -0.05, "noise": 0.12},
    "north_america": {**region("North America", "continent", [45, -100]), "ratio": 1.35, "offset": -0.02, "noise": 0.10},
    "europe": {**region("Europe", "continent", [50, 15]), "ratio": 1.45, "offset": -0.02, "noise": 0.10},
    "asia": {**region("Asia", "continent", [45, 90]), "ratio": 1.25, "offset": -0.02, "noise": 0.10},
    "africa": {**region("Africa", "continent", [0, 20]), "ratio": 0.95, "offset": 0.0, "noise": 0.07},
    "south_america": {**region("South America", "continent", [-15, -60]), "ratio": 0.85, "offset": 0.0, "noise": 0.07},
    "oceania": {**region("Oceania", "continent", [-25, 135]), "ratio": 0.80, "offset": 0.0, "noise": 0.07},
}


def temp_value(year: int, ratio: float, offset: float, noise: float) -> float:
    g0 = interp(TEMP_1980, TEMP_2024, 1980)
    g_year = interp(TEMP_1980, TEMP_2024, year)
    scaled = g0 + (g_year - g0) * ratio + offset
    return round(scaled + random.uniform(-noise, noise), 3)


temperature_json = {
    "display_name": "Global Temperature Anomaly",
    "description": "Surface temperature anomaly vs. 1951-1980 baseline.",
    "unit": "°C",
    "is_placeholder": True,
    "placeholder_note": (
        "The 'global' series is anchored to real published NASA GISTEMP figures "
        "(1980 \u2248 0.26\u00b0C, 2024 \u2248 1.28\u00b0C). Other regions apply an "
        "illustrative amplification ratio on top of that real curve, not measured "
        "regional data. Replace with fetch_real_data.py output before submission."
    ),
    "sources": [
        {
            "name": "NASA GISTEMP v4",
            "url": "https://data.giss.nasa.gov/gistemp/",
            "citation": "Lenssen et al. (2019), NASA GISS Surface Temperature Analysis",
        }
    ],
    "regions": {
        rid: {
            "name": r["name"],
            "type": r["type"],
            "coordinates": r["coordinates"],
            "time_series": [
                {
                    "year": y,
                    "value": temp_value(y, r["ratio"], r["offset"], r["noise"]),
                    "unit": "°C",
                }
                for y in YEARS
            ],
        }
        for rid, r in temp_regions.items()
    },
}

# ---------------------------------------------------------------------
# Sea Ice Extent (million km²)
# ---------------------------------------------------------------------
def arctic_series():
    return [
        {"year": y, "value": noisy(7.8, -0.075, y, 1980, 0.25), "unit": "million km²"}
        for y in YEARS
    ]


def antarctic_series():
    pts = []
    for y in YEARS:
        if y <= 2014:
            val = noisy(11.0, 0.02, y, 1980, 0.3)
        else:
            # Sharp reversal after 2014
            val_2014 = 11.0 + 0.02 * (2014 - 1980)
            val = noisy(val_2014, -0.28, y, 2014, 0.3)
        pts.append({"year": y, "value": val, "unit": "million km²"})
    return pts


sea_ice_json = {
    "display_name": "Sea Ice Extent",
    "description": "Arctic and Antarctic sea ice extent.",
    "unit": "million km²",
    "is_placeholder": True,
    "placeholder_note": "Synthetic demo data shaped to resemble NSIDC patterns. Replace before submission.",
    "sources": [
        {
            "name": "NSIDC Sea Ice Index v3",
            "url": "https://nsidc.org/data/seaice_index/",
            "citation": "Fetterer et al. (2017), National Snow and Ice Data Center",
        }
    ],
    "regions": {
        "arctic": {
            "name": "Arctic",
            "type": "custom",
            "coordinates": [75, 0],
            "time_series": arctic_series(),
        },
        "antarctic": {
            "name": "Antarctic",
            "type": "custom",
            "coordinates": [-75, 0],
            "time_series": antarctic_series(),
        },
    },
}

# ---------------------------------------------------------------------
# Atmospheric CO2 (ppm) - accelerating growth
# ---------------------------------------------------------------------
def co2_series():
    """Anchored to real 1980 (~338.7 ppm) and 2024 (~422.8 ppm) NOAA GML figures,
    with a slightly accelerating curve (quadratic term) between them, since real
    CO2 growth has been speeding up, not linear."""
    pts = []
    span = 2024 - 1980
    for i, y in enumerate(YEARS):
        t = i / span  # 0..1
        # Blend the real linear anchor with a mild acceleration curve (real
        # CO2 growth has sped up over the decades, not been perfectly linear),
        # while still hitting the same real 1980/2024 endpoints.
        value = CO2_1980 * (1 - t) + CO2_2024 * t + 3.0 * (t - t**2)
        value += random.uniform(-0.3, 0.3)
        pts.append({"year": y, "value": round(value, 2), "unit": "ppm"})
    return pts


co2_json = {
    "display_name": "Atmospheric CO2 Concentration",
    "description": "Global mean atmospheric CO2 concentration.",
    "unit": "ppm",
    "is_placeholder": True,
    "placeholder_note": (
        "Anchored to real published NOAA GML figures (1980 \u2248 338.7 ppm, "
        "2024 \u2248 422.8 ppm); the curve shape between those points and the "
        "month-to-month/year-to-year noise are illustrative, not the real "
        "recorded series. Replace with fetch_real_data.py output before submission."
    ),
    "sources": [
        {
            "name": "NOAA Global Monitoring Laboratory",
            "url": "https://gml.noaa.gov/ccgg/trends/",
            "citation": "NOAA GML, Mauna Loa Observatory CO2 record",
        }
    ],
    "regions": {
        "global": {
            "name": "Global",
            "type": "custom",
            "coordinates": [0, 0],
            "time_series": co2_series(),
        }
    },
}

FILES = {
    "temperature_anomaly.json": temperature_json,
    "sea_ice_extent.json": sea_ice_json,
    "co2_concentration.json": co2_json,
}

for filename, payload in FILES.items():
    path = DATA_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"✓ wrote {path} ({path.stat().st_size / 1024:.1f} KB)")

print("\nDone. These are SYNTHETIC placeholder datasets — see placeholder_note in each file.")
