import requests
import os
from hotelmate_onboarding.helper import read_config
import json

config = read_config()

s = requests.Session()


def businessServiceApi(propertyId, header):

    if os.environ['env_variable'] == 'TEST':
        businessServiceApi = config['TestApi']['businessserviceapi']
        BusinessTypeId=171
    elif os.environ['env_variable'] == 'PRODUCTION':
        businessServiceApi = config['ProductionApi']['businessserviceapi']
        BusinessTypeId=80
    else:
        raise ValueError("Invalid environment variable value")

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
    if businessService.status_code in [200,201]:
        
        data = businessService.content
        jsonData = json.loads(data)
        serviceId = jsonData['id']
        print("serviceId:", serviceId)
        print('businessService api status code', businessService.status_code)
    else:
        print('businessService api status code', businessService.status_code)
           
    return(serviceId, businessService.status_code)
