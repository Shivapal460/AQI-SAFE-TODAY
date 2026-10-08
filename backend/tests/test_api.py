from fastapi.testclient import TestClient

from app import main
from app.advisor import rule_based_advice
from app.aqi_client import aqi_label

client = TestClient(main.app)

FAKE_AIR = {
    "aqi": 180,
    "pm25": 95.0,
    "pm10": 150.0,
    "forecast": [{"time": "2026-10-08T18:00", "aqi": 180}],
}


def test_label_bands():
    assert aqi_label(30) == "Good"
    assert aqi_label(100) == "Moderate"
    assert aqi_label(180) == "Unhealthy"
    assert aqi_label(350) == "Hazardous"


def test_rules_are_stricter_for_sensitive_groups():
    child = rule_based_advice(120, "School child")
    adult = rule_based_advice(120, "Healthy adult")
    assert "N95" in child
    assert child != adult


def test_options_lists_areas_and_categories():
    body = client.get("/options").json()
    assert "Dwarka" in body["areas"]
    assert "Healthy adult" in body["categories"]


def test_advice_ok(monkeypatch):
    monkeypatch.setattr(main, "fetch_air_quality", lambda lat, lon: FAKE_AIR)
    monkeypatch.setattr(main, "get_advice", lambda *a, **k: ("Stay indoors.", "rules"))
    res = client.post("/advice", json={"area": "Dwarka", "category": "Healthy adult"})
    assert res.status_code == 200
    body = res.json()
    assert body["label"] == "Unhealthy"
    assert body["source"] == "rules"


def test_advice_unknown_area():
    res = client.post("/advice", json={"area": "Nowhere", "category": "Healthy adult"})
    assert res.status_code == 404
