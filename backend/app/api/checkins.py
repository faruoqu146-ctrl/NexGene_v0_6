from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.db.database import get_db
from app.db.models import Observation, ObservationType, User
from app.schemas import MorningCheckin, EveningCheckin, InsightResponse
from app.services.daily import build_insights, save_checkin_observations

router = APIRouter(prefix="/api/v1/checkins", tags=["checkins"])

@router.post("/morning")
def morning_checkin(
    payload: MorningCheckin,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recorded_at = payload.recorded_at or datetime.now(timezone.utc)
    save_checkin_observations(
        db,
        current_user.id,
        recorded_at,
        {
            "sleep_duration": payload.sleep_duration,
            "sleep_quality": payload.sleep_quality,
            "energy": payload.energy,
        },
    )
    return {"status": "ok", "recorded_at": recorded_at.isoformat()}

@router.post("/evening")
def evening_checkin(
    payload: EveningCheckin,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recorded_at = payload.recorded_at or datetime.now(timezone.utc)
    data = {
        "mood": payload.mood,
        "stress": payload.stress,
        "energy": payload.energy,
    }
    if payload.exercise_minutes is not None:
        data["exercise_minutes"] = payload.exercise_minutes
    if payload.symptoms:
        data["symptoms"] = payload.symptoms
    save_checkin_observations(db, current_user.id, recorded_at, data)
    return {"status": "ok", "recorded_at": recorded_at.isoformat()}

@router.get("/insights", response_model=list[InsightResponse])
def insights(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = (
        db.query(Observation, ObservationType)
        .join(ObservationType, Observation.observation_type_id == ObservationType.id)
        .filter(Observation.user_id == current_user.id)
        .order_by(Observation.recorded_at.asc())
        .all()
    )
    return build_insights(rows)
