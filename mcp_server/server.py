"""
FastMCP Server Entrypoint for Enterprise Property Onboarding.
Supports both local stdio mode (single PC) and HTTP/SSE mode (entire office / cloud).
"""
import sys
import os
from pathlib import Path

# Add project root to path and set CWD
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
os.chdir(project_root)

from dotenv import load_dotenv
load_dotenv(project_root / ".env")

from mcp.server.fastmcp import FastMCP
from mcp_server import tools

# Initialize FastMCP Server (configured for 0.0.0.0:8000 so entire office network can access)
mcp = FastMCP("Enterprise Property Onboarding Assistant", host="0.0.0.0", port=8000)


@mcp.tool()
def get_bookone_floor_standards() -> dict:
    """
    Returns the official reference of BookOne UI floor names and their required codes.
    Inspect this before building payloads to ensure floor names match BookOne standards
    ('Ground Floor' -> 'GF', 'First' -> '1st', 'Terrace Floor' -> 'Terrace').
    """
    return tools.get_bookone_floor_standards()


@mcp.tool()
def get_onboarding_sample_template() -> dict:
    """
    Returns a complete, pre-validated JSON template showing the correct format
    for rooms, floors, contact info, and pricing.
    """
    return tools.get_onboarding_sample_template()


@mcp.tool()
def preview_and_validate_property(property_data: dict) -> dict:
    """
    PRE-FLIGHT VALIDATION (Dry Run):
    Validates hotel data, checks floor mappings, room numbers, and pricing math
    BEFORE making any API calls or writing to the database.
    Always run this first to preview the setup and catch errors.
    """
    return tools.preview_and_validate_property(property_data)


@mcp.tool()
async def onboard_bookone_property(property_data: dict) -> dict:
    """
    EXECUTE BOOKONE ONBOARDING:
    Validates pre-flight conditions and executes the complete 17-step onboarding flow
    in TEST environment. Returns a sanitized enterprise summary with propertyId.
    """
    return await tools.onboard_bookone_property(property_data)


@mcp.tool()
async def onboard_hotelmate_property(property_data: dict) -> dict:
    """
    EXECUTE THEHOTELMATE ONBOARDING:
    Validates pre-flight conditions and executes onboarding for TheHotelMate
    in TEST environment. Returns a sanitized enterprise summary with propertyId.
    """
    return await tools.onboard_hotelmate_property(property_data)


if __name__ == "__main__":
    if "--sse" in sys.argv or "--http" in sys.argv:
        print("Starting FastMCP Server in SSE mode on http://0.0.0.0:8000/sse ...")
        mcp.run(transport="sse")
    else:
        mcp.run()
