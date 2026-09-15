# NexGene v0.6

Daily NexGene experience:
- authenticated user
- morning / evening check-ins
- chronological timeline
- simple longitudinal baseline insights
- mobile frontend

## Run locally (Docker)

```bash
docker compose up --build
```

- Mobile UI: http://localhost:8000/
- API docs:  http://localhost:8000/docs

## Test

```bash
# From project root
PYTHONPATH=backend pytest backend/tests -q

# Or inside the running container
docker compose exec api pytest -q
```

## Deploy on Render

1. Create a **PostgreSQL** database on Render. Copy the **Internal Database URL**.

2. Create a **Web Service**:
   - Connect the GitHub repo `faruoqu146-ctrl/NexGene_v0_6`
   - **Root Directory**: leave empty (repo root)
   - **Runtime**: Docker
   - **Dockerfile Path**: `Dockerfile`
   - **Instance type**: Free (or higher)

3. Environment variables:

   | Key            | Value                                      |
   |----------------|--------------------------------------------|
   | `DATABASE_URL` | Internal Database URL from step 1          |
   | `JWT_SECRET`   | a long random string                       |

4. Deploy. After it finishes you get a URL like:

   - App / mobile UI: `https://your-service.onrender.com/`
   - API docs:        `https://your-service.onrender.com/docs`

**Notes**
- Tables and observation types are created automatically on first startup.
- Free-tier services sleep after inactivity; the first request after sleep can take ~30–60 s.
- This is a development prototype. Do not use real patient, clinical, genetic, or production credentials.
- The insight engine is rule-based only. It is not medical advice.
