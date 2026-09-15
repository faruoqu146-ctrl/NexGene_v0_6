from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.db.database import get_db
from app.db.models import Observation, ObservationType, User

router = APIRouter(prefix="/api/v1/dev", tags=["dev"])

@router.get("/seed-status")
def seed_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    types = db.query(ObservationType).count()
    obs = db.query(Observation).filter(Observation.user_id == current_user.id).count()
    return {"observation_types": types, "user_observations": obs}
