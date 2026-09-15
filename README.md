# NexGene v0.6

Daily NexGene experience milestone:
- authenticated user
- morning check-in
- evening check-in
- chronological timeline
- simple longitudinal baseline insights
- mobile frontend (served at / and /mobile)

## Run
```bash
docker compose up --build
```

API docs: http://localhost:8000/docs
Mobile UI: http://localhost:8000/

## Test
```bash
# From project root
PYTHONPATH=backend pytest backend/tests -q
# Or with Docker
docker compose exec api pytest -q
```

This is a development prototype. Do not use real patient, clinical, genetic, or production credentials.
