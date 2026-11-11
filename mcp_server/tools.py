"""
Enterprise MCP Tools for BookOne and Hotelmate Property Onboarding.
Implements pre-flight validation, floor mapping verification, sanitized execution,
and post-onboard auditing.
"""
import sys
import os
import re
import copy
from pathlib import Path
from typing import Any, Dict, List
import requests

# Ensure parent directory is in sys.path so modules import seamlessly
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
os.chdir(project_root)

from dotenv import load_dotenv
load_dotenv(project_root / ".env")

# Global safeguard: enforce a 25-second default timeout on requests to prevent hanging Claude turns
_orig_session_request = requests.Session.request
def _timeout_guarded_request(self, *args, **kwargs):
    kwargs.setdefault('timeout', 25)
    return _orig_session_request(self, *args, **kwargs)
requests.Session.request = _timeout_guarded_request

from bookone_onboarding.Functions.roomDetails import resolve_floor, FLOOR_MAP
from bookone_onboarding.main import BookOneDriverClass
from hotelmate_onboarding.main import HotelmateDriverClass
from mcp_server.sanitizers import sanitize_onboarding_result, redact_sensitive_text


def clean_numeric_price(val: Any) -> int:
    """Safely converts price inputs (e.g. 2500, '2500', '₹2,500', '2,500') to integer."""
    if val is None:
        return 0
    if isinstance(val, (int, float)):
        return int(val)
    if isinstance(val, str):
        cleaned = re.sub(r"[^\d.]", "", val)
        if cleaned:
            return int(float(cleaned))
    return 0


def sanitize_property_pricing(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Safely normalizes string prices (e.g. '₹2,500' -> 2500) in property data
    so all onboarding functions receive clean numeric values without altering business logic.
    """
    safe_data = copy.deepcopy(data)
    if "extraPersonCharge" in safe_data:
        safe_data["extraPersonCharge"] = clean_numeric_price(safe_data.get("extraPersonCharge"))

    room_types = safe_data.get("roomType", {})
    if isinstance(room_types, dict):
        for r_name, r_conf in room_types.items():
            if isinstance(r_conf, dict):
                if "roomStandardPrice" in r_conf:
                    r_conf["roomStandardPrice"] = clean_numeric_price(r_conf.get("roomStandardPrice"))
                plans = r_conf.get("roomPlan", {})
                if isinstance(plans, dict):
                    for p_name, p_val in plans.items():
                        plans[p_name] = clean_numeric_price(p_val)
    return safe_data


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
    extra_charge = clean_numeric_price(property_data.get("extraPersonCharge", 0))
    total_room_price = 0
    for r_name, r_conf in room_types.items():
        if isinstance(r_conf, dict):
            std_price = clean_numeric_price(r_conf.get("roomStandardPrice", 0))
            if std_price <= 0:
                warnings.append(f"Standard price for '{r_name}' is not set or zero.")
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


# In-memory session cache for phased stage onboarding
ACTIVE_DRIVERS: Dict[str, Any] = {}


async def onboard_bookone_stage1_account(property_data: Dict[str, Any], ctx: Any = None) -> Dict[str, Any]:
    """
    STAGE 1 (Account Setup - Steps 01 to 05):
    Registers user account, sets admin profile, authenticates to acquire Property ID,
    resolves unique short name, and saves basic location info.
    """
    clean_data = sanitize_property_pricing(property_data)
    preflight = preview_and_validate_property(clean_data)
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
        driver = BookOneDriverClass([clean_data])
        res = await driver.stage_1()
        if res.get("status") != "success":
            return {
                "success": False,
                "platform": "BookOne",
                "environment": os.getenv("SERVER", "TEST"),
                "message": redact_sensitive_text(res.get("message", "Stage 1 failed"))
            }

        property_id = res["propertyId"]
        ACTIVE_DRIVERS[str(property_id)] = driver
        return {
            "success": True,
            "stage": 1,
            "platform": "BookOne",
            "environment": os.getenv("SERVER", "TEST"),
            "propertyId": property_id,
            "propertyName": res["businessName"],
            "loginEmail": res["businessEmail"],
            "message": f"Stage 1 Complete: Admin account registered. Property ID {property_id} assigned. Proceed to Stage 2."
        }
    except Exception as e:
        return {
            "success": False,
            "platform": "BookOne",
            "environment": os.getenv("SERVER", "TEST"),
            "propertyId": None,
            "businessName": clean_data.get("BusinessName", "Unknown"),
            "message": redact_sensitive_text(f"Execution error during Stage 1: {str(e)}")
        }


async def onboard_bookone_stage2_inventory(property_id: int, ctx: Any = None) -> Dict[str, Any]:
    """
    STAGE 2 (Inventory & Floors - Steps 06 to 10):
    Activates starter subscription, initializes rooms, registers room categories,
    fetches room IDs, and maps all room numbers across floors.
    """
    driver = ACTIVE_DRIVERS.get(str(property_id))
    if not driver:
        return {
            "success": False,
            "platform": "BookOne",
            "environment": os.getenv("SERVER", "TEST"),
            "message": f"Active onboarding session for Property ID {property_id} not found. Please run Stage 1 first."
        }

    try:
        res = await driver.stage_2()
        if res.get("status") != "success":
            return {
                "success": False,
                "platform": "BookOne",
                "environment": os.getenv("SERVER", "TEST"),
                "message": redact_sensitive_text(res.get("message", "Stage 2 failed"))
            }

        return {
            "success": True,
            "stage": 2,
            "platform": "BookOne",
            "environment": os.getenv("SERVER", "TEST"),
            "propertyId": property_id,
            "totalRooms": res["totalRooms"],
            "floors": res["floors"],
            "message": f"Stage 2 Complete: {res['totalRooms']} rooms mapped across {len(res['floors'])} floors. Proceed to Stage 3."
        }
    except Exception as e:
        return {
            "success": False,
            "platform": "BookOne",
            "environment": os.getenv("SERVER", "TEST"),
            "propertyId": property_id,
            "message": redact_sensitive_text(f"Execution error during Stage 2: {str(e)}")
        }


async def onboard_bookone_stage3_finalize(property_id: int, ctx: Any = None) -> Dict[str, Any]:
    """
    STAGE 3 (Rates, Taxes & Finalize - Steps 11 to 18):
    Generates yearly rates, attaches room plans, unlocks availability calendar,
    configures GST, business services, banking, payment modes, and activates property.
    Returns the final handover card.
    """
    driver = ACTIVE_DRIVERS.get(str(property_id))
    if not driver:
        return {
            "success": False,
            "platform": "BookOne",
            "environment": os.getenv("SERVER", "TEST"),
            "message": f"Active onboarding session for Property ID {property_id} not found. Please run Stage 1 and 2 first."
        }

    try:
        res = await driver.stage_3()
        ACTIVE_DRIVERS.pop(str(property_id), None)
        if res.get("status") != "success":
            return {
                "success": False,
                "platform": "BookOne",
                "environment": os.getenv("SERVER", "TEST"),
                "message": redact_sensitive_text(res.get("message", "Stage 3 failed"))
            }

        data_dict = driver.json_data[0] if isinstance(driver.json_data, list) else driver.json_data
        return sanitize_onboarding_result([res], data_dict, platform="BookOne")
    except Exception as e:
        return {
            "success": False,
            "platform": "BookOne",
            "environment": os.getenv("SERVER", "TEST"),
            "propertyId": property_id,
            "message": redact_sensitive_text(f"Execution error during Stage 3: {str(e)}")
        }


async def onboard_hotelmate_stage1_account(property_data: Dict[str, Any], ctx: Any = None) -> Dict[str, Any]:
    """STAGE 1 for TheHotelMate (Account Setup - Steps 01 to 05)."""
    clean_data = sanitize_property_pricing(property_data)
    preflight = preview_and_validate_property(clean_data)
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
        driver = HotelmateDriverClass([clean_data])
        res = await driver.stage_1()
        if res.get("status") != "success":
            return {
                "success": False,
                "platform": "TheHotelMate",
                "environment": os.getenv("SERVER", "TEST"),
                "message": redact_sensitive_text(res.get("message", "Stage 1 failed"))
            }

        property_id = res["propertyId"]
        ACTIVE_DRIVERS[str(property_id)] = driver
        return {
            "success": True,
            "stage": 1,
            "platform": "TheHotelMate",
            "environment": os.getenv("SERVER", "TEST"),
            "propertyId": property_id,
            "propertyName": res["businessName"],
            "loginEmail": res["businessEmail"],
            "message": f"Stage 1 Complete: Admin account registered. Property ID {property_id} assigned. Proceed to Stage 2."
        }
    except Exception as e:
        return {
            "success": False,
            "platform": "TheHotelMate",
            "environment": os.getenv("SERVER", "TEST"),
            "propertyId": None,
            "businessName": clean_data.get("BusinessName", "Unknown"),
            "message": redact_sensitive_text(f"Execution error during Stage 1: {str(e)}")
        }


async def onboard_hotelmate_stage2_inventory(property_id: int, ctx: Any = None) -> Dict[str, Any]:
    """STAGE 2 for TheHotelMate (Inventory & Floors - Steps 06 to 10)."""
    driver = ACTIVE_DRIVERS.get(str(property_id))
    if not driver:
        return {
            "success": False,
            "platform": "TheHotelMate",
            "environment": os.getenv("SERVER", "TEST"),
            "message": f"Active onboarding session for Property ID {property_id} not found. Please run Stage 1 first."
        }

    try:
        res = await driver.stage_2()
        if res.get("status") != "success":
            return {
                "success": False,
                "platform": "TheHotelMate",
                "environment": os.getenv("SERVER", "TEST"),
                "message": redact_sensitive_text(res.get("message", "Stage 2 failed"))
            }

        return {
            "success": True,
            "stage": 2,
            "platform": "TheHotelMate",
            "environment": os.getenv("SERVER", "TEST"),
            "propertyId": property_id,
            "totalRooms": res["totalRooms"],
            "floors": res["floors"],
            "message": f"Stage 2 Complete: {res['totalRooms']} rooms mapped across {len(res['floors'])} floors. Proceed to Stage 3."
        }
    except Exception as e:
        return {
            "success": False,
            "platform": "TheHotelMate",
            "environment": os.getenv("SERVER", "TEST"),
            "propertyId": property_id,
            "message": redact_sensitive_text(f"Execution error during Stage 2: {str(e)}")
        }


async def onboard_hotelmate_stage3_finalize(property_id: int, ctx: Any = None) -> Dict[str, Any]:
    """STAGE 3 for TheHotelMate (Rates, Taxes & Finalize - Steps 11 to 17)."""
    driver = ACTIVE_DRIVERS.get(str(property_id))
    if not driver:
        return {
            "success": False,
            "platform": "TheHotelMate",
            "environment": os.getenv("SERVER", "TEST"),
            "message": f"Active onboarding session for Property ID {property_id} not found. Please run Stage 1 and 2 first."
        }

    try:
        res = await driver.stage_3()
        ACTIVE_DRIVERS.pop(str(property_id), None)
        if res.get("status") != "success":
            return {
                "success": False,
                "platform": "TheHotelMate",
                "environment": os.getenv("SERVER", "TEST"),
                "message": redact_sensitive_text(res.get("message", "Stage 3 failed"))
            }

        data_dict = driver.jsonData[0] if isinstance(driver.jsonData, list) else driver.jsonData
        return sanitize_onboarding_result([res], data_dict, platform="TheHotelMate")
    except Exception as e:
        return {
            "success": False,
            "platform": "TheHotelMate",
            "environment": os.getenv("SERVER", "TEST"),
            "propertyId": property_id,
            "message": redact_sensitive_text(f"Execution error during Stage 3: {str(e)}")
        }


async def onboard_bookone_property(property_data: Dict[str, Any], ctx: Any = None) -> Dict[str, Any]:
    """
    EXECUTE BOOKONE ONBOARDING (All-in-One Batch Mode):
    Validates pre-flight conditions and executes all 18 onboarding steps sequentially.
    Returns the final handover card.
    """
    clean_data = sanitize_property_pricing(property_data)
    preflight = preview_and_validate_property(clean_data)
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
        driver = BookOneDriverClass([clean_data])
        raw_results = await driver.driverFunction()
        return sanitize_onboarding_result(raw_results, clean_data, platform="BookOne")
    except Exception as e:
        return {
            "success": False,
            "platform": "BookOne",
            "environment": os.getenv("SERVER", "TEST"),
            "propertyId": None,
            "businessName": clean_data.get("BusinessName", "Unknown"),
            "message": redact_sensitive_text(f"Execution error during BookOne onboarding: {str(e)}")
        }


async def onboard_hotelmate_property(property_data: Dict[str, Any], ctx: Any = None) -> Dict[str, Any]:
    """
    EXECUTE THEHOTELMATE ONBOARDING (All-in-One Batch Mode):
    Validates pre-flight conditions and executes all 17 onboarding steps sequentially.
    Returns the final handover card.
    """
    clean_data = sanitize_property_pricing(property_data)
    preflight = preview_and_validate_property(clean_data)
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
        driver = HotelmateDriverClass([clean_data])
        raw_results = await driver.driverFunction()
        return sanitize_onboarding_result(raw_results, clean_data, platform="TheHotelMate")
    except Exception as e:
        return {
            "success": False,
            "platform": "TheHotelMate",
            "environment": os.getenv("SERVER", "TEST"),
            "propertyId": None,
            "businessName": clean_data.get("BusinessName", "Unknown"),
            "message": redact_sensitive_text(f"Execution error during HotelMate onboarding: {str(e)}")
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
