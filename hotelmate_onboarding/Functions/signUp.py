import requests
import json
from hotelmate_onboarding.helper import read_config
import os

config = read_config()

s = requests.Session()

def signUp(businessEmail, password):

    userSingUpdata = {
        "plan": "Business Starter",
        "organisationId": 1,
        "businessType": "",
        "email": businessEmail,
        "password": password,
        "confirmPassword": password
    }
    print(config)
    if os.environ['env_variable'] == 'TEST':
        signupApi = config['TestApi']['signupapi']
    elif os.environ['env_variable'] == 'PRODUCTION':
        signupApi = config['ProductionApi']['signupapi']

    p = s.post(signupApi, json=userSingUpdata)
    signUpStatusCode = p.status_code

    if signUpStatusCode == 201:
        data = p.content
        jsonData = json.loads(data)
        userId = jsonData['id']
        signupData = {'signUpStatusCode': signUpStatusCode,
                      'userId': userId}
        return signupData, signUpStatusCode

    elif signUpStatusCode == 226:
        return {'message': 'Business Email Already exist!'}, signUpStatusCode

    else:
        # handle all other failures gracefully
        try:
            errorData = p.json()
        except Exception:
            errorData = p.text
        return {'message': 'Sign up failed', 'details': errorData}, signUpStatusCode

