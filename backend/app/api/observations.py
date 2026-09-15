from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.db.database import get_db
from app.db.models import Observation, ObservationType, User
from app.schemas import ObservationCreate, ObservationResponse

router = APIRouter(prefix="/api/v1/observations", tags=["observations"])

@router.post("", response_model=ObservationResponse, status_code=201)
def create_observation(
    payload: ObservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ot = db.query(ObservationType).filter(ObservationType.code == payload.observation_type).first()
    if not ot:
        raise HTTPException(status_code=400, detail=f"Unknown observation_type: {payload.observation_type}")
    obs = Observation(
        user_id=current_user.id,
        observation_type_id=ot.id,
        numeric_value=payload.numeric_value,
        text_value=payload.text_value,
        boolean_value=payload.boolean_value,
        recorded_at=payload.recorded_at,
    )
    db.add(obs)
    db.commit()
    db.refresh(obs)
    return ObservationResponse(
        id=obs.id,
        observation_type=ot.code,
        numeric_value=obs.numeric_value,
        text_value=obs.text_value,
        boolean_value=obs.boolean_value,
        recorded_at=obs.recorded_at,
    )

@router.get("", response_model=list[ObservationResponse])
def list_observations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = (
        db.query(Observation, ObservationType)
        .join(ObservationType, Observation.observation_type_id == ObservationType.id)
        .filter(Observation.user_id == current_user.id)
        .order_by(Observation.recorded_at.desc())
        .all()
    )
    return [
        ObservationResponse(
            id=obs.id,
            observation_type=ot.code,
            numeric_value=obs.numeric_value,
            text_value=obs.text_value,
            boolean_value=obs.boolean_value,
            recorded_at=obs.recorded_at,
        )
        for obs, ot in rows
    ]
