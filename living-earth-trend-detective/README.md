# Living Earth: Trend Detective

Built for **NASA Space Apps Challenge 2026** — *"Be An Earth System Trend Detective!"*

An interactive 3D globe for investigating NASA-measured environmental variables over
time, region by region, with real statistical rigor (Mann-Kendall trend test), and a
set of "Detective Cases" that explain why the same global process can drive opposite
trends in different regions.

> ⚠️ **Data status**: this repo ships with small, bundled JSON datasets in
> `backend/data/` so the app runs immediately with zero setup. **These are synthetic
> placeholder numbers**, shaped to resemble real NASA GISTEMP / NSIDC / NOAA patterns —
> they are *not* the real measurements. Every dataset file is tagged
> `"is_placeholder": true`. Before a real submission, replace them with actual NASA
> data — see [DATA_PIPELINE.md](./DATA_PIPELINE.md).

## Stack

- **Frontend**: React + TypeScript + Vite + Tailwind + `react-globe.gl` (Three.js) + Recharts + Zustand
- **Backend**: FastAPI, deployed as a single Vercel Python serverless function (via Mangum)
- **Stats**: Mann-Kendall trend test + Sen's slope (`pymannkendall`)
- **Data**: bundled local JSON by default; optional Cloudflare R2 (S3-compatible) for larger datasets

## Project structure

```
living-earth-trend-detective/
├── vercel.json              # Root deployment config
├── backend/
│   ├── api/                 # FastAPI routes + Vercel entry point (index.py)
│   ├── models/schemas.py    # Pydantic models
│   ├── services/            # data_loader.py, trend_analysis.py
│   ├── scripts/             # generate_dummy_data.py (synthetic placeholder data)
│   ├── data/                # bundled JSON datasets (committed, small)
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/      # Globe/, Charts/, Detective/, Landing/, UI/
    │   ├── pages/            # GlobeView, DetectiveView
    │   ├── services/api.ts
    │   ├── store/useGlobeStore.ts
    │   └── types/
    └── package.json
```

## Local development

### 1. Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt

# (Re)generate the bundled placeholder datasets
python scripts/generate_dummy_data.py

uvicorn api.index:app --reload --port 8000
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173** — the Vite dev server proxies `/api/*` to
`http://localhost:8000` (see `frontend/vite.config.ts`).

## Deploying to Vercel

1. Push this repo to GitHub.
2. In the Vercel dashboard, **Import Project** → select the repo.
   - Vercel reads `vercel.json` automatically: it builds `frontend/` as the static
     site and deploys `backend/api/index.py` as a Python serverless function.
   - No manual build/output directory configuration needed.
3. (Optional, only if you outgrow bundled JSON) Add environment variables for
   Cloudflare R2 — see `.env.example`. If left unset, the backend just reads the
   JSON files committed in `backend/data/`.
4. Deploy. Verify:
   - `https://<your-app>.vercel.app/api/health` → `{"status": "healthy", "layers_loaded": 3}`
   - The globe loads, layer toggle works, time slider works, clicking a region opens
     the trend panel, and `/detective` shows both cases.

### Local Vercel emulation (optional)

```bash
npm i -g vercel
vercel login
vercel link
vercel dev
```

## Replacing the placeholder data with real NASA data

See [DATA_PIPELINE.md](./DATA_PIPELINE.md) for the exact JSON schema each layer file
must follow, and where to pull real data from (NASA GISTEMP, NSIDC Sea Ice Index,
NOAA GML CO2 records).

## Submission checklist (NASA Space Apps specific)

- [ ] Replace synthetic data with real NASA/NOAA/NSIDC datasets
- [ ] Project page filled out on spaceappschallenge.org
- [ ] Public GitHub repo with this README, LICENSE, setup instructions
- [ ] Live demo URL (Vercel)
- [ ] NASA data source citations visible on screen (already implemented in the side panel)
- [ ] 2-3 min demo video

## License

MIT — see [LICENSE](./LICENSE). NASA data referenced here is public domain. This
project is not officially affiliated with or endorsed by NASA.
