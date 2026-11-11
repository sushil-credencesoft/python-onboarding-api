"""
Security and Output Sanitization Layer for MCP Server.
Ensures zero sensitive credentials (passwords, JWT tokens, internal secrets)
are ever exposed in tool responses or conversational logs.
"""
import copy
import os
import re
from typing import Any, Dict, List


def redact_sensitive_text(text: str) -> str:
    """
    Scans and redacts JWT tokens, passwords, user IDs, and sensitive strings
    from any error message or text output so nothing leaks to Claude.
    """
    if not isinstance(text, str):
        text = str(text)

    # Redact Bearer tokens
    text = re.sub(r'Bearer\s+[A-Za-z0-9\-_\.]+', 'Bearer [REDACTED_TOKEN]', text, flags=re.IGNORECASE)
    # Redact raw JWT tokens
    text = re.sub(r'ey[A-Za-z0-9\-_]{20,}\.[A-Za-z0-9\-_]{20,}\.[A-Za-z0-9\-_]{10,}', '[REDACTED_TOKEN]', text)
    # Redact passwords (e.g. Pass@1234, password="...")
    text = re.sub(r'(password[\'":\s=]+)([\w@#!$%^&*]+)', r'\1[REDACTED_PASSWORD]', text, flags=re.IGNORECASE)
    text = re.sub(r'Pass@\w+', '[REDACTED_PASSWORD]', text)
    # Redact internal user IDs (e.g. (ID: 1773), userId: 1773, USER_ID)
    text = re.sub(r'\(ID:\s*\d+\)', '', text)
    text = re.sub(r'(user_?id[\'":\s=]+)(\d+)', r'\1[REDACTED_USER_ID]', text, flags=re.IGNORECASE)

    return text


def get_login_portal_url(platform: str, env: str) -> str:
    """
    Returns the official portal login URL based on platform and environment.
    """
    env = (env or "TEST").upper()
    if platform.lower() == "bookone":
        default_url = "https://app-1.uat.bookonepms.com/#/sessions/signin" if env == "TEST" else "https://next.bookone.io/#/sessions/signin?return=%2F"
        return os.getenv("BOOKONE_LOGIN_URL", default_url)
    else:
        default_url = "https://uat.thehotelmate.co" if env == "TEST" else "https://app.thehotelmate.co"
        return os.getenv("HOTELMATE_LOGIN_URL", default_url)


def format_execution_log_table(raw_log: List[Dict[str, Any]]) -> str:
    """
    Renders the execution log into a clear Markdown audit table for Claude.
    """
    if not raw_log:
        return "No step logs recorded."

    lines = [
        "| Step | Operation | Status | Details |",
        "| :---: | :--- | :---: | :--- |"
    ]
    for entry in raw_log:
        step = entry.get("step", "--/--")
        name = entry.get("step_name", "Operation")
        status = entry.get("status", "UNKNOWN")
        details = redact_sensitive_text(entry.get("details", ""))

        if status == "SUCCESS":
            icon = "[SUCCESS]"
        elif status == "FAILED":
            icon = "[FAILED]"
        else:
            icon = "[IN_PROGRESS]"

        lines.append(f"| **{step}** | {name} | {icon} | {details} |")

    return "\n".join(lines)


def sanitize_onboarding_result(raw_results: Any, property_data: Dict[str, Any], platform: str = "BookOne") -> Dict[str, Any]:
    """
    Transforms internal driver execution results into a clean, enterprise-standard
    sanitized summary response with audit table.
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
    raw_execution_log: List[Dict[str, Any]] = []

    if isinstance(raw_results, list) and len(raw_results) > 0:
        first_item = raw_results[0]
        if isinstance(first_item, dict):
            raw_execution_log = first_item.get("execution_log", [])
            if first_item.get("status") == "success":
                is_success = True
                property_id = first_item.get("propertyId")
                message = f"Property '{business_name}' successfully onboarded to {platform}."
            else:
                is_success = False
                failed_step = first_item.get("failedStep")
                err_msg = first_item.get("message", "Error encountered during onboarding.")
                message = f"Failed at {failed_step}: {err_msg}" if failed_step else err_msg
        elif isinstance(first_item, str):
            if "already exist" in first_item.lower():
                is_success = False
                message = first_item
            else:
                message = str(first_item)
    elif isinstance(raw_results, dict):
        raw_execution_log = raw_results.get("execution_log", [])
        is_success = raw_results.get("status") == "success"
        property_id = raw_results.get("propertyId")
        message = raw_results.get("message", message)

    # Filter out duplicate IN_PROGRESS entries if a final SUCCESS/FAILED exists
    seen_steps = {}
    for entry in raw_execution_log:
        step_id = entry.get("step")
        seen_steps[step_id] = entry
    deduped_log = list(seen_steps.values())

    audit_table = format_execution_log_table(deduped_log if deduped_log else raw_execution_log)

    env = os.getenv("SERVER", "TEST")
    login_url = get_login_portal_url(platform, env)
    credential_notice = "Password will be sent to you via Email or WhatsApp."

    if is_success:
        message = (
            f"Property '{business_name}' successfully onboarded to {platform}!\n\n"
            f"### Account Access & Credential Details:\n"
            f"- **Property Name:** {business_name}\n"
            f"- **Property ID:** {property_id}\n"
            f"- **Login Email:** {business_email}\n"
            f"- **Login URL:** {login_url}\n"
            f"- **Access Notice:** {credential_notice}"
        )
    else:
        # User-friendly collision messages
        if "already exist" in message.lower() or "226" in message:
            message = (
                f"Onboarding halted: The email '{business_email}' is already registered in {platform}. "
                "Please provide a unique business email or update the existing property record."
            )
        elif "duplicate short name" in message.lower():
            message = (
                f"Onboarding halted: All generated short-name abbreviations for '{business_name}' "
                "are already in use. Please slightly modify the hotel name to proceed."
            )
        else:
            message = redact_sensitive_text(message)

    return {
        "success": is_success,
        "platform": platform,
        "environment": env,
        "propertyId": property_id,
        "businessName": business_name,
        "businessEmail": business_email,
        "loginUrl": login_url if is_success else None,
        "credentialNotice": credential_notice if is_success else None,
        "handover": {
            "propertyName": business_name,
            "propertyId": property_id,
            "loginEmail": business_email,
            "loginUrl": login_url,
            "notice": credential_notice
        } if is_success else None,
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
                if k == "accountNumber" and len(v) > 4:
                    d[k] = f"**** **** {v[-4:]}"
                else:
                    d[k] = "********"
            elif isinstance(v, dict):
                _mask_dict(v)

    if isinstance(safe, dict):
        _mask_dict(safe)
    return safe
