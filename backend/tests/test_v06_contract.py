from pathlib import Path

def test_mobile_frontend_exists():
    assert Path("mobile/index.html").exists() or Path("/mobile/index.html").exists()

def test_frontend_auth_and_checkins():
    text = Path("mobile/app.js").read_text()
    assert "Authorization" in text
    assert "/auth/${state.mode}" in text
    assert "/checkins/${mode}" in text

def test_v06_mount_and_health():
    text = Path("backend/app/main.py").read_text()
    assert 'version="0.6.0"' in text
    assert 'app.mount("/mobile"' in text
    assert '"version": "0.6.0"' in text
