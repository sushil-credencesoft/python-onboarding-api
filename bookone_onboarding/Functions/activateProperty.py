import os
import requests
from bookone_onboarding import helper

config = helper.read_config()
s = requests.Session()


def activateProperty(propertyId, userId, header):
    """
    Activates the property in BookOne:
    1. Fetches the complete property document via findbyuser endpoint.
    2. Sets 'active': True on the target property.
    3. Posts the updated property document to updateproperty endpoint.
    """
    env = os.environ.get('env_variable', 'PRODUCTION')
    section = 'TestApi' if env == 'TEST' else 'ProductionApi'

    find_by_user_url = config[section]['findbyuser'].replace('{userID}', str(userId)).replace('{userId}', str(userId))
    update_property_url = config[section]['updateproperty']

    # 1. Fetch user property object
    fetch_resp = s.get(find_by_user_url, headers=header)
    if fetch_resp.status_code not in (200, 201):
        print(f"Failed to fetch property for activation. Status code: {fetch_resp.status_code}")
        return fetch_resp.status_code

    data = fetch_resp.json()
    target_property = None
    if isinstance(data, list):
        for prop in data:
            if prop.get("id") == propertyId:
                target_property = prop
                break
        if not target_property and len(data) > 0:
            target_property = data[0]
    elif isinstance(data, dict):
        target_property = data

    if not target_property:
        print(f"Target property {propertyId} not found in findByUserId response")
        return 404

    # 2. Set active: True
    target_property["active"] = True

    # 3. Post updated property payload
    update_resp = s.post(update_property_url, headers=header, json=target_property)
    print(f"activate property status: {update_resp.status_code}")
    return update_resp.status_code
