import json
import requests
from hotelmate_onboarding.helper import read_config
import os

config = read_config()
s = requests.Session()

def login(email, password):
    loginPayload = {
        'username': email,
        'password': password
    }

    # Select correct login API based on environment
    env = os.environ.get('env_variable')
    if env == 'TEST':
        loginApi = config['TestApi']['loginapi']
    elif env == 'PRODUCTION':
        loginApi = config['ProductionApi']['loginapi']
    else:
        raise Exception(f"Invalid environment variable: {env}")

    # Make API call
    res = s.post(loginApi, json=loginPayload)

    # Check HTTP response status
    if res.status_code != 200:
        raise Exception(f"Login failed. Status code: {res.status_code}, Response: {res.text}")

    try:
        tokenData = res.json()  # parse JSON safely
    except json.JSONDecodeError:
        raise Exception(f"Login API did not return valid JSON. Raw response: {res.text}")

    # Ensure expected keys exist in response
    if 'token' not in tokenData or 'userId' not in tokenData or 'property' not in tokenData:
        raise KeyError(f"Missing expected keys in response: {tokenData}")

    # Set session header
    s.headers.update({'authorization': tokenData['token']})

    loginData = {
        'token': tokenData['token'],
        'userId': tokenData['userId'],
        'status-code': res.status_code,
        'propertyId': tokenData['property']['id']
    }

    print('Login api status code', res.status_code)

    return loginData
