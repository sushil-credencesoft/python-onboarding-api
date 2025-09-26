import requests
import os
from hotelmate_onboarding.helper import read_config
import json

config = read_config()

s = requests.Session()


def openDays(serviceId, header):

    if os.environ['env_variable'] == 'TEST':
        openDaysServiceApi = config['TestApi']['opendaysserviceapi']
    elif os.environ['env_variable'] == 'PRODUCTION':
        openDaysServiceApi = config['ProductionApi']['opendaysserviceapi']

    payload = [
        {
            "breakFromTime": "",
            "breakToTime": "",
            "openingTime": "06:00",
            "closingTime": "22:30",
            "day": "Sunday"
        },
        {
            "breakFromTime": "",
            "breakToTime": "",
            "openingTime": "06:00",
            "closingTime": "22:30",
            "day": "Monday"
        },
        {
            "breakFromTime": "",
            "breakToTime": "",
            "openingTime": "06:00",
            "closingTime": "22:30",
            "day": "Tuesday"
        },
        {
            "breakFromTime": "",
            "breakToTime": "",
            "openingTime": "06:00",
            "closingTime": "22:30",
            "day": "Wednesday"
        },
        {
            "breakFromTime": "",
            "breakToTime": "",
            "openingTime": "06:00",
            "closingTime": "22:30",
            "day": "Thursday"
        },
        {
            "breakFromTime": "",
            "breakToTime": "",
            "openingTime": "06:00",
            "closingTime": "22:30",
            "day": "Friday"
        },
        {
            "breakFromTime": "",
            "breakToTime": "",
            "openingTime": "06:00",
            "closingTime": "22:30",
            "day": "Saturday"
        }
    ]
    api = openDaysServiceApi.replace('{businessServiceId}', str(serviceId))
    print("businessServiceapi:" ,api)
    openDaysApiCall = s.post(api, headers=header, json=payload)
    print('open days api status code ', openDaysApiCall.status_code)

    return openDaysApiCall.status_code
