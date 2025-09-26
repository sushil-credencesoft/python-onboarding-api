import requests
import os
from bookone_onboarding import helper
import json

config = helper.read_config()

s = requests.Session()


def openDays(serviceId, header):

    if os.environ['env_variable'] == 'TEST':
        openDaysServiceApi = config['TestApi']['opendaysserviceapi'].replace(
            '{serviceID}', str(serviceId))
    elif os.environ['env_variable'] == 'PRODUCTION':
        openDaysServiceApi = config['ProductionApi']['opendaysserviceapi'].replace(
            '{serviceID}', str(serviceId))

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

    openDaysApiCall = s.post(openDaysServiceApi, headers=header, json=payload)
    print('open days api status code ', openDaysApiCall.status_code)

    return openDaysApiCall.status_code
