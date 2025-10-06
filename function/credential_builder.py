import os
import json

def create_credentials_file():
    cred_string = os.getenv("CRED_STRING")

    if not cred_string:
        print("Error: CRED_STRING not found in environment variables.")
        return

    try:
        creds = json.loads(cred_string)
        with open("credentials.json", "w", encoding="utf-8") as f:
            json.dump(creds, f, indent=4)
        print("credentials.json file created successfully!")
    except json.JSONDecodeError:
        print("Error: CRED_STRING is not a valid JSON string.")
