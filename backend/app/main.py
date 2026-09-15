from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.api import auth, checkins, dev, observations, profile, timeline

app = FastAPI(title="NexGene API", version="0.6.0")
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(observations.router)
app.include_router(checkins.router)
app.include_router(timeline.router)
app.include_router(dev.router)

MOBILE_DIR = Path("/mobile")
if MOBILE_DIR.exists():
    app.mount("/mobile", StaticFiles(directory=str(MOBILE_DIR)), name="mobile")

@app.get("/")
def root():
    index = MOBILE_DIR / "index.html"
    return FileResponse(index) if index.exists() else {"name": "NexGene", "version": "0.6.0"}

@app.get("/api/v1/health")
def health():
    return {"status": "ok", "version": "0.6.0"}
