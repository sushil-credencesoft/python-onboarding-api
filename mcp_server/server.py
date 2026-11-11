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

from mcp.server.fastmcp import FastMCP, Context
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
async def onboard_bookone_stage1_account(property_data: dict, ctx: Context = None) -> dict:
    """
    STAGE 1 OF 3 FOR BOOKONE (RECOMMENDED):
    Executes Steps 01 to 05 (Account sign up, profile setup, authentication, short name resolution,
    and basic property info). Finishes in ~7 seconds.
    Upon completion, output a brief update in chat and immediately call onboard_bookone_stage2_inventory.
    """
    return await tools.onboard_bookone_stage1_account(property_data, ctx=ctx)


@mcp.tool()
async def onboard_bookone_stage2_inventory(property_id: int, ctx: Context = None) -> dict:
    """
    STAGE 2 OF 3 FOR BOOKONE:
    Executes Steps 06 to 10 (Subscription activation, finish basic setup, room types, room IDs,
    and floor mappings). Finishes in ~9 seconds.
    Pass the 'propertyId' returned from Stage 1.
    Upon completion, output a brief update in chat and immediately call onboard_bookone_stage3_finalize.
    """
    return await tools.onboard_bookone_stage2_inventory(property_id, ctx=ctx)


@mcp.tool()
async def onboard_bookone_stage3_finalize(property_id: int, ctx: Context = None) -> dict:
    """
    STAGE 3 OF 3 FOR BOOKONE:
    Executes Steps 11 to 18 (Yearly rate matrix, room plans, calendar availability, GST, taxes,
    banking, payment modes, and property activation). Finishes in ~10 seconds.
    Pass the 'propertyId' from Stage 1.

    PRESENTATION GUIDELINES:
    - Do NOT include or print an Audit Log table.
    - Do NOT display any internal userId.
    - Present the final completion card containing:
      * Property Name
      * Property ID
      * Login Email
      * Login URL (exact URL from response 'loginUrl')
      * Access Notice: 'Password will be sent to you via Email or WhatsApp.'
    """
    return await tools.onboard_bookone_stage3_finalize(property_id, ctx=ctx)


@mcp.tool()
async def onboard_hotelmate_stage1_account(property_data: dict, ctx: Context = None) -> dict:
    """
    STAGE 1 OF 3 FOR THEHOTELMATE (RECOMMENDED):
    Executes Steps 01 to 05 for TheHotelMate. Finishes in ~7 seconds.
    Upon completion, output a brief update in chat and call onboard_hotelmate_stage2_inventory.
    """
    return await tools.onboard_hotelmate_stage1_account(property_data, ctx=ctx)


@mcp.tool()
async def onboard_hotelmate_stage2_inventory(property_id: int, ctx: Context = None) -> dict:
    """
    STAGE 2 OF 3 FOR THEHOTELMATE:
    Executes Steps 06 to 10 for TheHotelMate. Finishes in ~9 seconds.
    Pass the 'propertyId' returned from Stage 1.
    Upon completion, output a brief update in chat and call onboard_hotelmate_stage3_finalize.
    """
    return await tools.onboard_hotelmate_stage2_inventory(property_id, ctx=ctx)


@mcp.tool()
async def onboard_hotelmate_stage3_finalize(property_id: int, ctx: Context = None) -> dict:
    """
    STAGE 3 OF 3 FOR THEHOTELMATE:
    Executes Steps 11 to 17 for TheHotelMate. Finishes in ~10 seconds.
    Pass the 'propertyId' from Stage 1.

    PRESENTATION GUIDELINES:
    - Do NOT include or print an Audit Log table.
    - Do NOT display any internal userId.
    - Present the final completion card containing:
      * Property Name
      * Property ID
      * Login Email
      * Login URL (exact URL from response 'loginUrl')
      * Access Notice: 'Password will be sent to you via Email or WhatsApp.'
    """
    return await tools.onboard_hotelmate_stage3_finalize(property_id, ctx=ctx)


@mcp.tool()
async def onboard_bookone_property(property_data: dict, ctx: Context = None) -> dict:
    """
    EXECUTE BOOKONE ONBOARDING (All-in-One Batch Mode):
    Executes all 18 onboarding steps in a single call.
    Do NOT print an Audit Log table in the response. Output only the handover card:
    - Property Name
    - Property ID
    - Login Email
    - Login URL
    - Access Notice: 'Password will be sent to you via Email or WhatsApp.'
    """
    return await tools.onboard_bookone_property(property_data, ctx=ctx)


@mcp.tool()
async def onboard_hotelmate_property(property_data: dict, ctx: Context = None) -> dict:
    """
    EXECUTE THEHOTELMATE ONBOARDING (All-in-One Batch Mode):
    Executes all 17 onboarding steps in a single call.
    Do NOT print an Audit Log table in the response. Output only the handover card:
    - Property Name
    - Property ID
    - Login Email
    - Login URL
    - Access Notice: 'Password will be sent to you via Email or WhatsApp.'
    """
    return await tools.onboard_hotelmate_property(property_data, ctx=ctx)


if __name__ == "__main__":
    if "--sse" in sys.argv or "--http" in sys.argv:
        print("Starting FastMCP Server in SSE mode on http://0.0.0.0:8000/sse ...")
        mcp.run(transport="sse")
    else:
        mcp.run()
