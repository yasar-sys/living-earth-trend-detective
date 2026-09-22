# Data Pipeline

The backend loads three JSON files, one per layer, from `backend/data/`
(or from Cloudflare R2 if the `R2_*` env vars are set — see `services/data_loader.py`).

## Required schema (per layer file)

```json
{
  "display_name": "Global Temperature Anomaly",
  "description": "Surface temperature anomaly vs. 1951-1980 baseline.",
  "unit": "°C",
  "is_placeholder": false,
  "sources": [
    {
      "name": "NASA GISTEMP v4",
      "url": "https://data.giss.nasa.gov/gistemp/",
      "citation": "Lenssen et al. (2019), NASA GISS Surface Temperature Analysis"
    }
  ],
  "regions": {
    "global": {
      "name": "Global",
      "type": "custom",
      "coordinates": [0, 0],
      "time_series": [
        { "year": 1980, "value": -0.18, "unit": "°C" },
        { "year": 1981, "value": -0.05, "unit": "°C" }
      ]
    },
    "arctic": { "...": "..." }
  }
}
```

Notes:
- `coordinates` is `[lat, lon]`, used to place the region's marker on the globe.
- `time_series` should ideally be annual and gap-free; the Mann-Kendall test in
  `services/trend_analysis.py` needs at least 8 points per region to compute a trend.
- File names must match `models/schemas.py::DataLayer` values exactly:
  `temperature_anomaly.json`, `sea_ice_extent.json`, `co2_concentration.json`.

## Where to get real data

| Layer | Source | Notes |
|---|---|---|
| Temperature Anomaly | [NASA GISTEMP v4](https://data.giss.nasa.gov/gistemp/) | CSV downloads by region/zone available directly |
| Sea Ice Extent | [NSIDC Sea Ice Index](https://nsidc.org/data/seaice_index/) | Monthly Arctic/Antarctic extent, aggregate to annual mean |
| CO2 Concentration | [NOAA GML Trends](https://gml.noaa.gov/ccgg/trends/) | Mauna Loa + global mean, monthly, aggregate to annual mean |

## Suggested ETL steps

1. Download the raw CSV/text files from the sources above.
2. Clean and aggregate to **annual** values per region (pandas is already a
   reasonable choice, though it isn't in `requirements.txt` by default — add
   `pandas` if your ETL script needs it; the backend itself doesn't require it).
3. Compute `coordinates` centroids for each region you include.
4. Write out JSON matching the schema above, one file per layer, into `backend/data/`.
5. Set `"is_placeholder": false` once real data is in place.
6. (Optional) If your files grow large (multi-MB), move them to Cloudflare R2 instead
   of committing to git — set the `R2_*` environment variables from `.env.example` and
   the backend will automatically prefer R2 over the local files. A small
   `scripts/upload_to_r2.py` helper is not included by default since the bundled
   local-JSON path is enough for hackathon-scale datasets — add one only if you
   actually need it.

## Regenerating the placeholder data

```bash
cd backend
python scripts/generate_dummy_data.py
```

This is deterministic (seeded) and safe to re-run. The "global" series in
each layer is anchored to a couple of real published figures (2024 global
temperature anomaly ≈ 1.28°C, 2024 global CO2 ≈ 422.8 ppm), but everything
else — the curve shape between anchors, other regions, sea ice — is still
illustrative, not the real recorded series.

## Fetching the REAL data (do this before submission)

```bash
cd backend
pip install -r requirements-dev.txt   # adds requests + pandas
python scripts/fetch_real_data.py
```

Run this on your own machine (not a restricted sandbox) — it needs normal
internet access to `data.giss.nasa.gov`, `gml.noaa.gov`, and
`noaadata.apps.nsidc.org`. It overwrites `backend/data/*.json` with the real
NASA GISTEMP, NOAA GML CO2, and NSIDC sea ice records, and sets
`"is_placeholder": false`.

**Check before you rely on it**: NSIDC occasionally changes their exact file
layout/URLs — if `fetch_sea_ice()` fails, visit
https://nsidc.org/data/seaice_index/ and update `SEAICE_URLS` in the script
to the current download links. The script prints a clear warning per-dataset
if a fetch fails rather than silently writing bad data.
