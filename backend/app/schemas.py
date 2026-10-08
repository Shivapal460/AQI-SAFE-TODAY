from pydantic import BaseModel


class AdviceRequest(BaseModel):
    area: str
    category: str


class ForecastPoint(BaseModel):
    time: str
    aqi: float


class AdviceResponse(BaseModel):
    area: str
    aqi: float
    label: str
    pm25: float
    pm10: float
    forecast: list[ForecastPoint]
    advice: str
    source: str  # "ai" or "rules"
