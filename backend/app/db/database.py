import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def _normalize_database_url(url: str) -> str:
    """Render and many hosts give postgres:// — SQLAlchemy + psycopg need postgresql+psycopg://."""
    if url.startswith("postgres://"):
        url = "postgresql+psycopg://" + url[len("postgres://") :]
    elif url.startswith("postgresql://") and "+psycopg" not in url:
        url = "postgresql+psycopg://" + url[len("postgresql://") :]
    return url


DATABASE_URL = _normalize_database_url(
    os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://nexgene:nexgene_dev_only@localhost:5432/nexgene",
    )
)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create tables and seed observation types (safe to run on every startup)."""
    from app.db.models import Base, ObservationType

    Base.metadata.create_all(bind=engine)

    seeds = [
        ("sleep_duration", "Sleep duration", "hours"),
        ("sleep_quality", "Sleep quality", None),
        ("energy", "Energy", None),
        ("mood", "Mood", None),
        ("stress", "Stress", None),
        ("focus", "Focus", None),
        ("activity_duration", "Activity duration", "minutes"),
        ("weight", "Weight", "kg"),
        ("heart_rate", "Heart rate", "bpm"),
        ("hrv", "Heart rate variability", "ms"),
        ("blood_pressure_systolic", "Blood pressure systolic", "mmHg"),
        ("blood_pressure_diastolic", "Blood pressure diastolic", "mmHg"),
        ("glucose", "Glucose", "mg/dL"),
        ("temperature", "Temperature", "C"),
    ]

    db = SessionLocal()
    try:
        for code, name, unit in seeds:
            exists = db.query(ObservationType).filter(ObservationType.code == code).first()
            if not exists:
                db.add(ObservationType(code=code, name=name, unit=unit))
        db.commit()
    finally:
        db.close()
