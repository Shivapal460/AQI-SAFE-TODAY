# Is it safe outside today?

Built for Environmental Hacks (WeMakeDevs x AWS, Bharat Builds Tour), Air track.

Everyone in Delhi NCR can see the AQI number, but most people do not know what it means for them. A reading that is fine for a healthy adult can be risky for a school child or an elderly person. This app takes the live AQI for an area and the type of person asking, and returns short, practical advice: whether to go out, which mask to wear, and what to do about school or exercise.

## Features

- Live AQI, PM2.5 and PM10 for areas across Delhi NCR
- 12 hour AQI trend chart
- Advice tailored to a school child, senior citizen, runner or healthy adult
- Works even if the AI model is unavailable, using built-in rules

## Tech stack

- Backend: Python, FastAPI
- Frontend: Streamlit
- Data: Open-Meteo Air Quality API
- AI: Strands Agents SDK (AWS open source), Amazon Bedrock or a local Ollama model

## Project structure

    backend/    FastAPI service (AQI data and advice)
    frontend/   Streamlit web app
    docs/       Architecture notes

## Running locally

You need Python 3.10 or newer. Use two terminals.

Backend:

    cd backend
    pip install -r requirements-dev.txt
    python -m uvicorn app.main:app --reload --port 8000

API docs are available at http://localhost:8000/docs

Frontend:

    cd frontend
    pip install -r requirements.txt
    python -m streamlit run app.py

If the backend runs somewhere else, set the API_URL environment variable.

## AI model setup

By default the Strands agent uses Amazon Bedrock, which needs AWS credentials and model access. Without that, the backend uses its rule-based advice and the app shows which source was used.

To use a local model instead, install Ollama, pull a model, then:

    pip install "strands-agents[ollama]"

and set USE_OLLAMA=1 (see backend/.env.example).

## Tests

    cd backend
    python -m pytest

## Limitations

- Areas are a fixed list of points, not station-level readings
- AQI is on the US scale, which differs a little from the Indian CPCB index
- The advice is general guidance and not medical advice

## Team

- <Name> (backend)
- <Name> (frontend)
- <Name> (docs and demo)
