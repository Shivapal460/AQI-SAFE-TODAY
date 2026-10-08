import os

import pandas as pd
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Is it safe outside today?")
st.title("Is it safe outside today?")
st.caption("Live air quality for Delhi NCR, with advice based on who you are.")


@st.cache_data(ttl=3600)
def load_options():
    resp = requests.get(f"{API_URL}/options", timeout=10)
    resp.raise_for_status()
    return resp.json()


try:
    options = load_options()
except requests.RequestException:
    st.error(f"Could not reach the backend at {API_URL}. Is it running?")
    st.stop()

area = st.selectbox("Area", options["areas"])
category = st.selectbox("Who is this for?", options["categories"])

if st.button("Check air quality"):
    with st.spinner("Fetching live data..."):
        try:
            resp = requests.post(
                f"{API_URL}/advice",
                json={"area": area, "category": category},
                timeout=120,
            )
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as exc:
            st.error(f"Request failed: {exc}")
            st.stop()

    col1, col2, col3 = st.columns(3)
    col1.metric("AQI (US)", round(data["aqi"]), data["label"])
    col2.metric("PM2.5", data["pm25"])
    col3.metric("PM10", data["pm10"])

    st.subheader("Next 12 hours")
    forecast = pd.DataFrame(data["forecast"])
    forecast["time"] = pd.to_datetime(forecast["time"])
    st.line_chart(forecast.set_index("time")["aqi"])

    st.subheader("Advice")
    if data["aqi"] <= 100:
        st.success(data["advice"])
    elif data["aqi"] <= 150:
        st.warning(data["advice"])
    else:
        st.error(data["advice"])

    source = "AI agent" if data["source"] == "ai" else "built-in rules"
    st.caption(f"Advice from: {source}. Air quality data: Open-Meteo (US AQI scale).")
