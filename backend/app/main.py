from fastapi import FastAPI, HTTPException

from .advisor import get_advice
from .aqi_client import AirQualityError, aqi_label, fetch_air_quality
from .config import AREAS, CATEGORIES
from .schemas import AdviceRequest, AdviceResponse

app = FastAPI(title="Air Quality Advisor API", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/options")
def options():
    return {"areas": list(AREAS), "categories": CATEGORIES}


@app.post("/advice", response_model=AdviceResponse)
def advice(req: AdviceRequest):
    if req.area not in AREAS:
        raise HTTPException(status_code=404, detail="Unknown area")
    if req.category not in CATEGORIES:
        raise HTTPException(status_code=400, detail="Unknown category")

    lat, lon = AREAS[req.area]
    try:
        air = fetch_air_quality(lat, lon)
    except AirQualityError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    label = aqi_label(air["aqi"])
    text, source = get_advice(req.area, req.category, air, label)
    return AdviceResponse(
        area=req.area,
        aqi=air["aqi"],
        label=label,
        pm25=air["pm25"],
        pm10=air["pm10"],
        forecast=air["forecast"],
        advice=text,
        source=source,
    )
