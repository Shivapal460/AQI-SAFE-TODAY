import requests

from .config import OPEN_METEO_URL


class AirQualityError(Exception):
    pass


def fetch_air_quality(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "us_aqi,pm2_5,pm10",
        "hourly": "us_aqi",
        "forecast_days": 2,
        "timezone": "Asia/Kolkata",
    }
    try:
        resp = requests.get(OPEN_METEO_URL, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        current = data["current"]
        times = data["hourly"]["time"]
        values = data["hourly"]["us_aqi"]
    except (requests.RequestException, KeyError, ValueError) as exc:
        raise AirQualityError(f"Could not read air quality data: {exc}") from exc

    if current.get("us_aqi") is None:
        raise AirQualityError("No current AQI reading for this location")

    # Hourly data starts at midnight, so find the current hour first
    now_hour = current["time"][:13]
    start = next((i for i, t in enumerate(times) if t[:13] >= now_hour), 0)
    forecast = [
        {"time": t, "aqi": v}
        for t, v in zip(times[start:start + 12], values[start:start + 12])
        if v is not None
    ]

    return {
        "aqi": current["us_aqi"],
        "pm25": current["pm2_5"],
        "pm10": current["pm10"],
        "forecast": forecast,
    }


def aqi_label(aqi):
    if aqi <= 50:
        return "Good"
    if aqi <= 100:
        return "Moderate"
    if aqi <= 150:
        return "Unhealthy for sensitive groups"
    if aqi <= 200:
        return "Unhealthy"
    if aqi <= 300:
        return "Very unhealthy"
    return "Hazardous"
