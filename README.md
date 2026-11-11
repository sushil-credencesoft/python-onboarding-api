# Python Onboarding API

FastAPI service and MCP tools for onboarding BookOne and TheHotelMate properties.

## Run the REST API

From the repository root, install the dependencies in `requirements.txt`, configure the required local environment and credentials, then run:

```powershell
uvicorn onboarding_api.main:app --host 127.0.0.1 --port 8000
```

The existing `uvicorn main:app` entry point remains available for compatibility.

## REST routes

- `POST /api/onboard/bookOne`
- `POST /api/onboard/theHotelMate`
- Storage routes remain under `/api/storage`.

The onboarding body follows `onboarding_api.schemas.onboard.OnboardingData`. Use the existing sample payload in `ultimate.json` as a format reference.

## MCP entry points

- `python -m mcp_server.server` starts the full onboarding MCP server in stdio mode.
- `python -m mcp_server.server --http` starts its HTTP/SSE transport.
- `python mcp_server.py` remains the legacy, basic stdio server.

The MCP and REST interfaces call the same existing platform driver packages (`bookone_onboarding` and `hotelmate_onboarding`).

## Package layout

- `onboarding_api/main.py`: FastAPI application entry point.
- `onboarding_api/api/routes/`: REST route modules.
- `onboarding_api/schemas/`: request schemas.
- `bookone_onboarding/`, `hotelmate_onboarding/`: existing platform drivers and integrations.
- `mcp_server/`: MCP server, tools, and response sanitizers.
- `router/`, `models/`, root `main.py`: compatibility import paths for existing consumers.

Keep `.env`, GCP credentials, and platform secrets outside source control. The current REST API does not add service-to-service authentication in this structural refactor; deploy it only behind an appropriately restricted network until that is implemented.
