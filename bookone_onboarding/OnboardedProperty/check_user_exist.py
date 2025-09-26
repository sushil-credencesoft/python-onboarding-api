import json
from pathlib import Path

import requests


def get_project_root() -> Path:
    return Path(__file__).parent.parent


root = get_project_root()

file = open(f"Onboarding/OnboardedProperty/properties_to_be_onboarded.txt")
emails = file.read().split()
file.close()

request = requests.Session()
bearer_token_test = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJpbmZvQGJvb2tvbmVwbXMuY29tIiwic2NvcGVzIjoiUk9MRV9PUkdfQURNSU4iLCJpYXQiOjE2ODg2NDExNDUsImV4cCI6MTY4OTA3MzE0NX0.t9xzWvi8Gf4U1YytlyCpSAdYwNqF_TJrm1jX4TyFcvA"
bearer_token_production = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbkBib29rb25lbG9jYWwuaW4iLCJzY29wZXMiOiJST0xFX09SR19BRE1JTiIsImlhdCI6MTY5ODc0NDg0MSwiZXhwIjoxNjk5MTc2ODQxfQ.Fo9Ps_cMDBUkdpidipcKnClWanYChjJezlEwQMn4eQg"
token = None
api = None
# server = 'test'
server = 'prod'

if server == 'test':
    api = f"https://testapi.bookonelocal.co.nz/api-bookone/api/user/organisation/{1}"
    token = bearer_token_test
    header = {
        'USER_ID': "2",
        'Authorization': token,
        'APP_ID': 'BOOKONE_WEB_APP'
    }
    api_response = request.get(api, headers=header).content
    api_data = json.loads(api_response)
    existing_emails = []
    for i in range(len(api_data)):
        property_ = api_data[i]
        existing_emails.append(property_["email"])

    properties_can_file = open(f"{root}/OnboardedProperty/properties_can_be_onboard.txt", mode='w')
    properties_can_not_file = open(f"{root}/OnboardedProperty/properties_can_not_be_onboard.txt", mode='w')

    email_exist = []
    for email in emails:
        for exist_email in existing_emails:
            if email == exist_email:
                properties_can_not_file.write(email + '\n')
                email_exist.append(email)
                break

    for email in emails:
        for exist_email in email_exist:
            if email != exist_email:
                properties_can_file.write(email + '\n')

else:
    api = f"https://api.bookonelocal.in/api-bookone/api/user/organisation/{1}"
    token = bearer_token_production
    header = {
        'USER_ID': "2",
        'Authorization': token,
        'APP_ID': 'BOOKONE_WEB_APP'
    }
    api_response = request.get(api, headers=header).content
    api_data = json.loads(api_response)

    existing_emails = []
    for i in range(len(api_data)):
        property_ = api_data[i]
        existing_emails.append(property_["email"])

    properties_can_file = open(f"{root}/OnboardedProperty/properties_can_be_onboard.txt", mode='w')
    properties_can_not_file = open(f"{root}/OnboardedProperty/properties_can_not_be_onboard.txt", mode='w')

    email_exist = []
    for email in emails:
        for exist_email in existing_emails:
            if email == exist_email:
                properties_can_not_file.write(email + '\n')
                email_exist.append(email)
                break

    for email in emails:
        if len(email_exist) == 0:
            properties_can_file.write(email + '\n')
            break
        count = existing_emails.count(email)
        if count == 0:
            properties_can_file.write(email + '\n')

    properties_can_file.close()
    properties_can_not_file.close()
