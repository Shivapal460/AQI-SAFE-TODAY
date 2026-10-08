import logging

from .config import OLLAMA_HOST, OLLAMA_MODEL, USE_OLLAMA

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are an air quality advisor for people living in Delhi NCR. "
    "Given the current readings and the user's category, reply in plain English "
    "in at most five short lines. Cover whether it is safe to be outside, "
    "which mask to wear (if any), what to do about school or exercise, and how "
    "the next few hours look. Do not give medical diagnoses. If the user has "
    "serious symptoms, tell them to see a doctor."
)

SENSITIVE = {"School child", "Senior citizen (60+)"}


def rule_based_advice(aqi, category):
    """Simple fallback used when the AI model is not available."""
    sensitive = category in SENSITIVE
    runner = category.startswith("Runner")

    if aqi <= 50:
        return "Air quality is good. Normal outdoor activity is fine."
    if aqi <= 100:
        if sensitive:
            return ("Air quality is acceptable. Keep long outdoor stretches short "
                    "and stay off busy roads.")
        return "Air quality is acceptable. Normal outdoor activity is fine."
    if aqi <= 150:
        if sensitive:
            return ("Air is unhealthy for sensitive groups. Limit time outdoors "
                    "and wear an N95 mask if you go out.")
        if runner:
            return ("Keep the run light and short, or move it indoors. "
                    "Avoid busy roads.")
        return "Fine for most people, but cut down on long or intense outdoor activity."
    if aqi <= 200:
        if sensitive:
            return ("Stay indoors as much as possible and wear an N95 mask when you "
                    "must go out. Skip outdoor play and sports.")
        if runner:
            return ("Skip outdoor exercise today and train indoors. Wear an N95 mask "
                    "for any outdoor errands.")
        return "Reduce time outdoors and wear an N95 mask if you go out."
    return ("Air quality is very poor. Stay indoors with windows closed, and wear an "
            "N95 mask for any unavoidable trip outside.")


def _build_agent():
    from strands import Agent

    if USE_OLLAMA:
        from strands.models.ollama import OllamaModel

        model = OllamaModel(host=OLLAMA_HOST, model_id=OLLAMA_MODEL)
        return Agent(model=model, system_prompt=SYSTEM_PROMPT)
    return Agent(system_prompt=SYSTEM_PROMPT)


def get_advice(area, category, air, label):
    """Returns (advice, source). source is "ai" or "rules"."""
    trend = ", ".join(f"{p['time'][11:16]}={round(p['aqi'])}" for p in air["forecast"])
    question = (
        f"Area: {area}\n"
        f"User category: {category}\n"
        f"Current US AQI: {round(air['aqi'])} ({label})\n"
        f"PM2.5: {air['pm25']}, PM10: {air['pm10']}\n"
        f"AQI over the next 12 hours: {trend}\n"
        "Give today's advice for this user."
    )
    try:
        reply = str(_build_agent()(question)).strip()
        if reply:
            return reply, "ai"
    except Exception as exc:
        logger.warning("AI advice failed, using rules instead: %s", exc)
    return rule_based_advice(air["aqi"], category), "rules"
