from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.api import auth, checkins, dev, observations, profile, timeline
from app.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="NexGene API", version="0.6.0", lifespan=lifespan)
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(observations.router)
app.include_router(checkins.router)
app.include_router(timeline.router)
app.include_router(dev.router)

# Resolve mobile frontend for local, Docker, and Render
_candidates = [
    Path("/mobile"),
    Path(__file__).resolve().parents[2] / "mobile",
    Path(__file__).resolve().parents[1] / "mobile",
    Path("mobile"),
]
MOBILE_DIR = next((p for p in _candidates if p.is_dir()), None)

if MOBILE_DIR is not None:
    app.mount("/mobile", StaticFiles(directory=str(MOBILE_DIR)), name="mobile")


@app.get("/")
def root():
    if MOBILE_DIR is not None:
        index = MOBILE_DIR / "index.html"
        if index.exists():
            return FileResponse(index)
    return {"name": "NexGene", "version": "0.6.0"}


@app.get("/api/v1/health")
def health():
    return {"status": "ok", "version": "0.6.0"}
