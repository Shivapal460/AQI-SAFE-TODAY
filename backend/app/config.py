import os

from dotenv import load_dotenv

load_dotenv()

OPEN_METEO_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

# Approximate centre point of each area (lat, lon)
AREAS = {
    "Greater Noida": (28.4744, 77.5040),
    "Connaught Place": (28.6315, 77.2167),
    "Dwarka": (28.5921, 77.0460),
    "Rohini": (28.7383, 77.0822),
    "Anand Vihar": (28.6469, 77.3164),
    "Saket": (28.5245, 77.2066),
}

CATEGORIES = [
    "School child",
    "Senior citizen (60+)",
    "Runner / outdoor exerciser",
    "Healthy adult",
]

# Strands talks to Amazon Bedrock by default.
# Set USE_OLLAMA=1 to use a local model instead.
USE_OLLAMA = os.getenv("USE_OLLAMA") == "1"
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
