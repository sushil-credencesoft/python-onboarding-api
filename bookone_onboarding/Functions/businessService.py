import requests
import os
from bookone_onboarding import helper
import json

config = helper.read_config()

s = requests.Session()


def businessServiceApi(propertyId, header):

    if os.environ['env_variable'] == 'TEST':
        businessServiceApi = config['TestApi']['businessserviceapi']
        BusinessTypeId=171
    elif os.environ['env_variable'] == 'PRODUCTION':
        businessServiceApi = config['ProductionApi']['businessserviceapi']
        BusinessTypeId=80

    businessServ = {
        "sendInstantConfirmation": True,
        "fontAwesomeUrl": "",
        "name": "Accommodation",
        "groupName": "TRAVEL & TOURISM",
        "code": "01",
        "organisationId": 1,
        "businessTypeId": BusinessTypeId,
        "bookingButtonLabelText": "Accomodation",
        "businessLocationName": "Accomodation",
        "businessProductName": "Accomodation",
        "businessServiceName": "Tours and Travels",
        "businessTermLocation": "",
        "businessTermResource": "",
        "canChangeBusinessAddress": True,
        "customerLocationName": "Accomodation",
        "provideBusinessAndCustomerAddress": True,
        "propertyId": propertyId
    }

    businessService = s.post(
        businessServiceApi, json=businessServ, headers=header)
    businessServiceStatusCode = businessService.status_code
    data = businessService.content
    jsonData = json.loads(data)
    serviceId = jsonData['id']
    if businessServiceStatusCode == 200:
        print('businessService api status code', businessServiceStatusCode)

    return (serviceId, businessServiceStatusCode)
