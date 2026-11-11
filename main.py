"""Backward-compatible ASGI entry point.

Run with ``uvicorn main:app`` as before. New deployments may use
``uvicorn onboarding_api.main:app``.
"""
from onboarding_api.main import *  # noqa: F401,F403


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("onboarding_api.main:app", host="127.0.0.1", port=8000, reload=True)
