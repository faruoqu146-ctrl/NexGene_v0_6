from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.db.database import get_db
from app.db.models import Observation, ObservationType, User
from app.schemas import ObservationResponse

router = APIRouter(prefix="/api/v1/timeline", tags=["timeline"])

@router.get("", response_model=list[ObservationResponse])
def timeline(
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
