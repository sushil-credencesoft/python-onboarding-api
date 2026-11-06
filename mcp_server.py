from dotenv import load_dotenv
load_dotenv()

import json
import logging
from mcp.server.fastmcp import FastMCP
from bookone_onboarding.main import BookOneDriverClass
from hotelmate_onboarding.main import HotelmateDriverClass

# Initialize FastMCP Server
mcp = FastMCP("Property-Onboarding-Server")


@mcp.tool()
async def onboard_bookone_property(property_data: dict) -> str:
    """
    Onboard a new hotel/property to BookOne.
    Requires full property details: BusinessName, address, email, mobile, roomType, and roomDetails.
    """
    try:
        driver = BookOneDriverClass([property_data])
        results = await driver.driverFunction()
        return json.dumps(results, indent=2)
    except Exception as e:
        return f"Error during BookOne onboarding: {str(e)}"


@mcp.tool()
async def onboard_hotelmate_property(property_data: dict) -> str:
    """
    Onboard a new hotel/property to Hotelmate.
    Requires full property details: BusinessName, address, email, mobile, roomType, and roomDetails.
    """
    try:
        driver = HotelmateDriverClass([property_data])
        results = await driver.driverFunction()
        return json.dumps(results, indent=2)
    except Exception as e:
        return f"Error during Hotelmate onboarding: {str(e)}"


@mcp.tool()
def get_sample_onboarding_template() -> dict:
    """
    Returns the required JSON schema/template for property onboarding.
    Use this to see how roomType, roomDetails, and contact fields must be formatted.
    """
    with open("ultimate.json", "r", encoding="utf-8") as f:
        return json.load(f)[0]


if __name__ == "__main__":
    mcp.run()
