from pathlib import Path
import requests
import time
import json


def get_project_root() -> Path:
    return Path(__file__).parent.parent


root = get_project_root()
request = requests.Session()

# Get all Property Email
property_file = open(f"{root}/OnboardedProperty/properties.txt")
properties_emails = property_file.read().split()
property_file.close()

# Get The Sequence Number
sequence_file = open(f"{root}/OnboardedProperty/sequence.txt")
sequence = sequence_file.read()
sequence_file.close()

onboarded_property_file = open(f"{root}/OnboardedProperty/onboardedproperties.txt", mode='a')

if sequence == "":
    sequence = 1
else:
    sequence = int(sequence)

for hotel in properties_emails:
    email = hotel
    password = "Pass@1234"

    login_api = "https://api.thehotelmate.co/api/user/login"
    login_payload = {
        "username": email,
        "password": password
    }

    login_response = request.post(login_api, json=login_payload)
    if login_response.status_code == 401:
        print(f"login_response status code {login_response.status_code}")
        onboarded_property_file.write(f"{sequence}/Password Changed: {email}\n")
        sequence += 1
    elif login_response.status_code == 200:
        login_response_ = login_response.content
        time.sleep(5)
        login_response_data = json.loads(login_response_)
        token = f'Bearer {login_response_data["token"]}'
        userId = login_response_data["userId"]
        propertyId = str(login_response_data["property"]["id"])

        header = {
            'USER_ID': str(userId),
            'Authorization': token,
            'APP_ID': 'BOOKONE_WEB_APP'
        }

        property_api = f"https://api.thehotelmate.co/api/property/findById/{propertyId}"

        property_response = request.get(property_api, headers=header).content
        property_response_data = json.loads(property_response)
        property_name = property_response_data["name"]

        onboarded_property_file.write(
            f'{sequence}/ Hotel Name = "{property_name}" and Email = "{email}"\n')
        sequence += 1

onboarded_property_file.close()
sequence_file = open(f"{root}/OnboardedProperty/sequence.txt", mode='w')
sequence_file.write(str(sequence))
sequence_file.close()