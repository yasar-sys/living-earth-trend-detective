"""
Fetches the REAL NASA/NOAA/NSIDC datasets and writes them into the exact
JSON schema this backend expects (see DATA_PIPELINE.md).

Run this on YOUR OWN machine, not inside a restricted sandbox — it needs
normal internet access to data.giss.nasa.gov, gml.noaa.gov and nsidc.org.

Usage:
    pip install requests pandas
    python backend/scripts/fetch_real_data.py

This will overwrite backend/data/*.json with real data and set
"is_placeholder": false.
"""
import io
import json
from pathlib import Path

import pandas as pd
import requests

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

HEADERS = {"User-Agent": "living-earth-trend-detective/1.0 (hackathon project)"}


# ---------------------------------------------------------------------
# 1. NASA GISTEMP - Global + Northern/Southern Hemisphere temperature anomaly
# ---------------------------------------------------------------------
GISTEMP_URLS = {
    "global": "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv",
    "north_hemisphere": "https://data.giss.nasa.gov/gistemp/tabledata_v4/NH.Ts+dSST.csv",
    "south_hemisphere": "https://data.giss.nasa.gov/gistemp/tabledata_v4/SH.Ts+dSST.csv",
}


def fetch_gistemp() -> dict:
    print("Fetching NASA GISTEMP...")
    regions = {}
    names = {
        "global": ("Global", [0, 0]),
        "north_hemisphere": ("Northern Hemisphere", [45, 0]),
        "south_hemisphere": ("Southern Hemisphere", [-45, 0]),
    }

    for key, url in GISTEMP_URLS.items():
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        # GISTEMP CSVs have a title line before the real header row.
        df = pd.read_csv(io.StringIO(resp.text), skiprows=1)
        df = df[["Year", "J-D"]].rename(columns={"J-D": "value"})
        df = df[df["value"] != "***"]
        df["value"] = df["value"].astype(float)

        name, coords = names[key]
        regions[key] = {
            "name": name,
            "type": "custom",
            "coordinates": coords,
            "time_series": [
                {"year": int(row.Year), "value": round(float(row.value), 3), "unit": "°C"}
                for row in df.itertuples()
            ],
        }

    return {
        "display_name": "Global Temperature Anomaly",
        "description": "Surface temperature anomaly vs. 1951-1980 baseline.",
        "unit": "°C",
        "is_placeholder": False,
        "sources": [
            {
                "name": "NASA GISTEMP v4",
                "url": "https://data.giss.nasa.gov/gistemp/",
                "citation": "Lenssen et al. (2019), NASA GISS Surface Temperature Analysis",
            }
        ],
        "regions": regions,
    }


# ---------------------------------------------------------------------
# 2. NOAA GML - Global mean CO2
# ---------------------------------------------------------------------
CO2_URL = "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_gl.txt"


def fetch_co2() -> dict:
    print("Fetching NOAA GML CO2...")
    resp = requests.get(CO2_URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()

    rows = []
    for line in resp.text.splitlines():
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split()
        # columns: year  mean  unc
        year, mean = int(parts[0]), float(parts[1])
        rows.append({"year": year, "value": mean, "unit": "ppm"})

    return {
        "display_name": "Atmospheric CO2 Concentration",
        "description": "Global mean atmospheric CO2 concentration.",
        "unit": "ppm",
        "is_placeholder": False,
        "sources": [
            {
                "name": "NOAA Global Monitoring Laboratory",
                "url": "https://gml.noaa.gov/ccgg/trends/",
                "citation": "NOAA GML, global mean CO2 (marine surface network)",
            }
        ],
        "regions": {
            "global": {
                "name": "Global",
                "type": "custom",
                "coordinates": [0, 0],
                "time_series": rows,
            }
        },
    }


# ---------------------------------------------------------------------
# 3. NSIDC Sea Ice Index - Arctic & Antarctic monthly extent -> annual mean
# ---------------------------------------------------------------------
# NSIDC publishes per-region CSVs of daily/monthly extent. The exact file
# layout changes occasionally - check https://nsidc.org/data/seaice_index/
# for the current download links and adjust SEAICE_URLS if needed.
SEAICE_URLS = {
    "arctic": "https://noaadata.apps.nsidc.org/NOAA/G02135/north/monthly/data/N_09_extent_v3.0.csv",
    "antarctic": "https://noaadata.apps.nsidc.org/NOAA/G02135/south/monthly/data/S_09_extent_v3.0.csv",
}


def fetch_sea_ice() -> dict:
    print("Fetching NSIDC Sea Ice Index (September extent, annual minimum proxy)...")
    regions = {}
    names = {"arctic": ("Arctic", [75, 0]), "antarctic": ("Antarctic", [-75, 0])}

    for key, url in SEAICE_URLS.items():
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        df = pd.read_csv(io.StringIO(resp.text), skipinitialspace=True)
        df.columns = [c.strip() for c in df.columns]
        # NSIDC monthly CSVs have columns like: year, mo, data-type, region, extent, area
        df = df[["year", "extent"]].rename(columns={"year": "Year", "extent": "value"})

        name, coords = names[key]
        regions[key] = {
            "name": name,
            "type": "custom",
            "coordinates": coords,
            "time_series": [
                {"year": int(row.Year), "value": round(float(row.value), 3), "unit": "million km²"}
                for row in df.itertuples()
            ],
        }

    return {
        "display_name": "Sea Ice Extent",
        "description": "September (annual minimum) Arctic and Antarctic sea ice extent.",
        "unit": "million km²",
        "is_placeholder": False,
        "sources": [
            {
                "name": "NSIDC Sea Ice Index v3",
                "url": "https://nsidc.org/data/seaice_index/",
                "citation": "Fetterer et al. (2017), National Snow and Ice Data Center",
            }
        ],
        "regions": regions,
    }


def main():
    datasets = {
        "temperature_anomaly.json": fetch_gistemp,
        "co2_concentration.json": fetch_co2,
        "sea_ice_extent.json": fetch_sea_ice,
    }

    for filename, fetcher in datasets.items():
        try:
            payload = fetcher()
        except Exception as exc:  # noqa: BLE001
            print(f"⚠️  Failed to fetch {filename}: {exc}")
            print("    Check the source URL is still valid and retry.")
            continue

        path = DATA_DIR / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        print(f"✓ wrote real data to {path}")

    print("\nDone. Remember to also update the region ratios elsewhere in the")
    print("app (e.g. detective case narratives) if the real trends differ")
    print("meaningfully from the placeholder assumptions.")


if __name__ == "__main__":
    main()
