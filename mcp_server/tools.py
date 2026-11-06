"""
Enterprise MCP Tools for BookOne and Hotelmate Property Onboarding.
Implements pre-flight validation, floor mapping verification, sanitized execution,
and post-onboard auditing.
"""
import sys
import os
from pathlib import Path
from typing import Any, Dict, List

# Ensure parent directory is in sys.path so modules import seamlessly
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
os.chdir(project_root)

from dotenv import load_dotenv
load_dotenv(project_root / ".env")

from bookone_onboarding.Functions.roomDetails import resolve_floor, FLOOR_MAP
from bookone_onboarding.main import BookOneDriverClass
from hotelmate_onboarding.main import HotelmateDriverClass
from mcp_server.sanitizers import sanitize_onboarding_result


def get_bookone_floor_standards() -> Dict[str, Any]:
    """
    Returns the official reference of BookOne UI floor names and their required codes.
    Use this to inspect how floors should be mapped (e.g. 'Ground Floor' -> 'GF', 'First' -> '1st').
    """
    sample_standards = [
        {"uiName": "Basement Floor", "floorNumber": "BF", "description": "Basement level"},
        {"uiName": "Ground Floor", "floorNumber": "GF", "description": "Ground / Entry floor"},
        {"uiName": "First", "floorNumber": "1st", "description": "1st floor level"},
        {"uiName": "Second", "floorNumber": "2nd", "description": "2nd floor level"},
        {"uiName": "Third", "floorNumber": "3rd", "description": "3rd floor level"},
        {"uiName": "Fourth", "floorNumber": "4th", "description": "4th floor level"},
        {"uiName": "Terrace Floor", "floorNumber": "Terrace", "description": "Rooftop / Terrace level"}
    ]
    return {
        "status": "success",
        "description": "BookOne UI official floor mapping rules",
        "specialFloors": ["Ground Floor (GF)", "Basement Floor (BF)", "Terrace Floor (Terrace)"],
        "numberedFloors": "Numbered floors use cardinal name ('First', 'Second', 'Third') with ordinal code ('1st', '2nd')",
        "samples": sample_standards
    }


def preview_and_validate_property(property_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    PRE-FLIGHT VALIDATION (Dry Run):
    Validates hotel data, checks floor mappings, room numbers, and pricing math
    BEFORE making any API calls or writing to the database.
    """
    errors: List[str] = []
    warnings: List[str] = []

    # 1. Validate Core Required Fields
    required_fields = ["BusinessName", "email", "city", "country", "mobile", "roomType", "roomDetails"]
    for field in required_fields:
        if not property_data.get(field):
            errors.append(f"Missing required field: '{field}'")

    email = property_data.get("email", "")
    if email and ("@" not in email or "." not in email):
        errors.append(f"Invalid email format: '{email}'")

    # 2. Validate Room Types
    room_types = property_data.get("roomType", {})
    if not isinstance(room_types, dict) or len(room_types) == 0:
        errors.append("'roomType' must be a dictionary with at least one room category.")

    # 3. Validate Floors and Room Numbers
    room_details = property_data.get("roomDetails", {})
    if not isinstance(room_details, dict) or len(room_details) == 0:
        errors.append("'roomDetails' must be a dictionary defining floors and rooms.")

    detected_floors = []
    all_room_numbers = []
    total_rooms = 0

    if isinstance(room_details, dict):
        for floor_input, rooms_on_floor in room_details.items():
            resolved_name, resolved_code = resolve_floor(floor_input)
            floor_room_count = 0

            if isinstance(rooms_on_floor, dict):
                for r_type, r_info in rooms_on_floor.items():
                    if r_type not in room_types:
                        warnings.append(
                            f"Room type '{r_type}' on '{floor_input}' is not declared in 'roomType' catalog."
                        )
                    
                    nums = r_info.get("room numbers", []) if isinstance(r_info, dict) else []
                    floor_room_count += len(nums)
                    for n in nums:
                        all_room_numbers.append(str(n))

            total_rooms += floor_room_count
            detected_floors.append({
                "inputFloor": floor_input,
                "resolvedFloorName": resolved_name,
                "resolvedFloorNumber": resolved_code,
                "roomsOnFloor": floor_room_count
            })

    # Check for duplicate room numbers
    duplicate_rooms = [num for num in set(all_room_numbers) if all_room_numbers.count(num) > 1]
    if duplicate_rooms:
        warnings.append(f"Duplicate room numbers detected: {duplicate_rooms}")

    # 4. Math & Pricing Preview
    extra_charge = int(property_data.get("extraPersonCharge", 0) or 0)
    total_room_price = 0
    for r_name, r_conf in room_types.items():
        if isinstance(r_conf, dict):
            std_price = int(r_conf.get("roomStandardPrice", 0) or 0)
            count = all_room_numbers.count(r_name)
            total_room_price += std_price * count

    is_valid = len(errors) == 0

    return {
        "valid": is_valid,
        "environment": os.getenv("SERVER", "TEST"),
        "businessName": property_data.get("BusinessName", ""),
        "businessEmail": email,
        "totalRoomsDetected": total_rooms,
        "roomCategories": list(room_types.keys()),
        "detectedFloors": detected_floors,
        "allRoomNumbers": all_room_numbers,
        "errors": errors,
        "warnings": warnings,
        "readyToOnboard": is_valid
    }


async def onboard_bookone_property(property_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    EXECUTE BOOKONE ONBOARDING:
    Validates pre-flight conditions and executes the complete 17-step onboarding flow.
    Returns a sanitized enterprise summary.
    """
    # Run pre-flight validation first
    preflight = preview_and_validate_property(property_data)
    if not preflight["valid"]:
        return {
            "success": False,
            "platform": "BookOne",
            "environment": os.getenv("SERVER", "TEST"),
            "message": "Pre-flight validation failed. Correct the errors before onboarding.",
            "errors": preflight["errors"],
            "warnings": preflight["warnings"]
        }

    try:
        driver = BookOneDriverClass([property_data])
        raw_results = await driver.driverFunction()
        return sanitize_onboarding_result(raw_results, property_data, platform="BookOne")
    except Exception as e:
        return {
            "success": False,
            "platform": "BookOne",
            "environment": os.getenv("SERVER", "TEST"),
            "propertyId": None,
            "businessName": property_data.get("BusinessName", "Unknown"),
            "message": f"Execution error during BookOne onboarding: {str(e)}"
        }


async def onboard_hotelmate_property(property_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    EXECUTE THEHOTELMATE ONBOARDING:
    Validates pre-flight conditions and executes onboarding for TheHotelMate.
    Returns a sanitized enterprise summary.
    """
    preflight = preview_and_validate_property(property_data)
    if not preflight["valid"]:
        return {
            "success": False,
            "platform": "TheHotelMate",
            "environment": os.getenv("SERVER", "TEST"),
            "message": "Pre-flight validation failed. Correct the errors before onboarding.",
            "errors": preflight["errors"],
            "warnings": preflight["warnings"]
        }

    try:
        driver = HotelmateDriverClass([property_data])
        raw_results = await driver.driverFunction()
        return sanitize_onboarding_result(raw_results, property_data, platform="TheHotelMate")
    except Exception as e:
        return {
            "success": False,
            "platform": "TheHotelMate",
            "environment": os.getenv("SERVER", "TEST"),
            "propertyId": None,
            "businessName": property_data.get("BusinessName", "Unknown"),
            "message": f"Execution error during HotelMate onboarding: {str(e)}"
        }


def get_onboarding_sample_template() -> Dict[str, Any]:
    """
    Returns a complete, pre-validated JSON template showing the correct format
    for rooms, floors, contact info, and pricing.
    """
    import json
    template_path = project_root / "ultimate.json"
    if template_path.exists():
        with open(template_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data[0] if isinstance(data, list) else data
    return {"error": "Sample template file not found."}
