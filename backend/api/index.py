import os
import sys
from pathlib import Path

# Make sibling packages (models/, services/) importable regardless of
# how Vercel's Python builder resolves the working directory.
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from mangum import Mangum  # noqa: E402

from api.detective import router as detective_router  # noqa: E402
from api.layers import router as layers_router  # noqa: E402
from api.trends import router as trends_router  # noqa: E402
from services.data_loader import get_data_loader  # noqa: E402

app = FastAPI(
    title="Living Earth: Trend Detective API",
    description="NASA Space Apps 2026 - Be An Earth System Trend Detective!",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

_static_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]
_frontend_url = os.getenv("FRONTEND_URL")
if _frontend_url:
    _static_origins.append(_frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_static_origins,
    # Matches every Vercel preview + production deployment URL.
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(layers_router, prefix="/api")
app.include_router(trends_router, prefix="/api")
app.include_router(detective_router, prefix="/api")


@app.get("/api/health")
async def health():
    loader = get_data_loader()
    return {"status": "healthy", "layers_loaded": len(loader.get_all_meta())}


# Vercel calls this `handler` for the Python runtime.
handler = Mangum(app, lifespan="off")
