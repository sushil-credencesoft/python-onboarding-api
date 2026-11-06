"""
Security and Output Sanitization Layer for MCP Server.
Ensures zero sensitive credentials (passwords, JWT tokens, internal secrets)
are ever exposed in tool responses or conversational logs.
"""
import copy
from typing import Any, Dict, List


def sanitize_onboarding_result(raw_results: Any, property_data: Dict[str, Any], platform: str = "BookOne") -> Dict[str, Any]:
    """
    Transforms internal driver execution results into a clean, enterprise-standard
    sanitized summary response.
    """
    business_name = property_data.get("BusinessName", "Unknown Property")
    business_email = property_data.get("email", "N/A")
    room_details = property_data.get("roomDetails", {})

    # Extract clean list of floors and rooms
    floors_summary = list(room_details.keys())
    total_rooms = 0
    room_numbers_list: List[str] = []

    for floor_key, room_dict in room_details.items():
        if isinstance(room_dict, dict):
            for room_type, details in room_dict.items():
                if isinstance(details, dict):
                    nums = details.get("room numbers", [])
                    total_rooms += len(nums)
                    room_numbers_list.extend([str(n) for n in nums])

    # Check for errors in raw result
    is_success = False
    property_id = None
    message = "Onboarding execution finished."

    if isinstance(raw_results, list) and len(raw_results) > 0:
        first_item = raw_results[0]
        if isinstance(first_item, dict):
            if first_item.get("status") == "success":
                is_success = True
                property_id = first_item.get("propertyId")
                message = f"Property '{business_name}' successfully onboarded to {platform}."
            else:
                is_success = False
                message = first_item.get("message", "Error encountered during onboarding.")
        elif isinstance(first_item, str):
            if "already exist" in first_item.lower():
                is_success = False
                message = first_item
            else:
                message = str(first_item)
    elif isinstance(raw_results, dict):
        is_success = raw_results.get("status") == "success"
        property_id = raw_results.get("propertyId")
        message = raw_results.get("message", message)

    return {
        "success": is_success,
        "platform": platform,
        "environment": "TEST",
        "propertyId": property_id,
        "businessName": business_name,
        "businessEmail": business_email,
        "summary": {
            "totalRoomsConfigured": total_rooms,
            "floorsConfigured": floors_summary,
            "roomNumbers": room_numbers_list,
        },
        "message": message
    }


def mask_sensitive_fields(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Returns a safe copy of property data with passwords and sensitive bank data masked.
    """
    safe = copy.deepcopy(data)
    sensitive_keys = {"password", "confirmPassword", "accountNumber", "swiftCode", "token", "Authorization"}

    def _mask_dict(d: Dict[str, Any]):
        for k, v in d.items():
            if k in sensitive_keys and isinstance(v, str) and v:
                d[k] = "********"
            elif isinstance(v, dict):
                _mask_dict(v)

    if isinstance(safe, dict):
        _mask_dict(safe)
    return safe
