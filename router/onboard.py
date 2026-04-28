from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any, List
import logging
import json

from hotelmate_onboarding.main import HotelmateDriverClass
from bookone_onboarding.main import BookOneDriverClass
from models.onboard import OnboardingData

onboard = APIRouter(prefix="/api/onboard", tags=["Onboarding-router"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@onboard.post("/theHotelMate")
async def start_onboarding(data: OnboardingData):
    try:
        logger.info("[INFO] Received data for onboarding")
        driver = HotelmateDriverClass([data.dict(by_alias=True)])
        results = await driver.driverFunction()

        #  ADD THIS LINE (main fix)
        if not results:
            return JSONResponse(status_code=500, content={
                "error": "Empty results from driver",
                "results": []
            })

        # Check for errors safely
        if any(isinstance(item, dict) and item.get("status") == "error" for item in results):
            return JSONResponse(status_code=500, content={
                "error": results[0] if isinstance(results[0], dict) else results
            })

        # Return success safely
        return JSONResponse(status_code=200, content={
            "results": results[0] if isinstance(results[0], dict) else results
        })

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@onboard.post("/bookOne")
async def start_onboarding(data: OnboardingData):
    try:
        logger.info("[INFO] Received data for onboarding")
        driver = BookOneDriverClass([data.dict(by_alias=True)])
        results = await driver.driverFunction()

        # # Check for errors in results
        # if any(item.get("status") == "error" for item in results):
        #     return JSONResponse(status_code=500, content={results[0]['results']})
        # return JSONResponse(status_code=200, content={results[0]['results']})
        # Check for errors safely
        if any(isinstance(item, dict) and item.get("status") == "error" for item in results):
            return JSONResponse(status_code=500, content={
                "error": results[0] if isinstance(results[0], dict) else results[0]
            })
        # Return success safely
        return JSONResponse(status_code=200, content={
            "results": results[0] if isinstance(results[0], dict) else results
        })


    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
