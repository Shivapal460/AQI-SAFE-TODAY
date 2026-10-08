# Architecture

## Flow

    Streamlit frontend  --HTTP-->  FastAPI backend  -->  Open-Meteo (live AQI)
                                          |
                                          +-->  Strands agent (advice)
                                                  |-- Amazon Bedrock (default)
                                                  |-- Ollama (local, optional)
                                                  +-- rule-based fallback

## Backend endpoints

| Method | Path     | Purpose                                          |
|--------|----------|--------------------------------------------------|
| GET    | /health  | Liveness check                                   |
| GET    | /options | Areas and user categories for the dropdowns      |
| POST   | /advice  | Live AQI, 12 hour trend and advice for one user  |

## Design notes

- The frontend holds no business logic. Areas and categories come from the backend,
  so adding an area only needs a change in backend/app/config.py.
- If the AI model cannot be reached, the backend falls back to rule-based advice,
  so the app still returns something useful. The response says which one was used.
- AQI values use the US scale from Open-Meteo, which differs slightly from the
  Indian CPCB index.

## Possible next steps

- Deploy the backend on AWS Lambda behind API Gateway
- Add more areas, or let the user search any location
- Add CPCB station data for better local accuracy
