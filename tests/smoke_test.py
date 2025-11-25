# tests/smoke_test.py
import requests, time
def test_health():
    r = requests.get("http://localhost:8000/docs")
    assert r.status_code in (200, 404)
