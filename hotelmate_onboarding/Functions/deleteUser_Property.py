import requests
import os
from hotelmate_onboarding.helper import read_config

config = read_config()

s = requests.Session()


def delet_user_and_property(header, propertyId):
    if os.environ['env_variable'] == 'TEST':
        delete_property_api = config['TestApi']['deletepropertyapi'].replace(
            '{propertyId}', str(propertyId))
        delete_user_api = config['TestApi']['deleteuserapi'].replace(
            '{propertyId}', str(propertyId))
    elif os.environ['env_variable'] == 'PRODUCTION':
        delete_property_api = config['ProductionApi']['deletepropertyapi'].replace(
            '{propertyId}', str(propertyId))
        delete_user_api = config['ProductionApi']['deleteuserapi'].replace(
            '{propertyId}', str(propertyId))

    delete_user_apicall = s.post(delete_user_api, headers=header)
    print("delete user api status code ", delete_user_apicall.status_code)

    if delete_user_apicall.status_code==200:
        delete_property_apicall = s.post(delete_property_api, headers=header)
        print("delete property api status code",
            delete_property_apicall.status_code)
    else:
        print('Property can not be deleted because user is not deleted!')

    return None
