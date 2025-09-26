import requests
import os
from bookone_onboarding import helper

config = helper.read_config()

s = requests.Session()


def addRoom(propertyId, header, roomType, count):

    if os.environ['env_variable'] == 'TEST':
        addRoomApi = config['TestApi']['addroomapi'].replace(
            '{propertyId}', str(propertyId))
    elif os.environ['env_variable'] == 'PRODUCTION':
        addRoomApi = config['ProductionApi']['addroomapi'].replace(
            '{propertyId}', str(propertyId))

    typesOfRoom = list(roomType.keys())
    for i in range(0, len(typesOfRoom)):
        addRoomPayload = {
            "name": typesOfRoom[i],
            "propertyId": propertyId,
            "roomOnlyPrice": roomType[typesOfRoom[i]]['roomStandardPrice'],
            "minimumOccupancy": 2,
            "maximumOccupancy": 4,
            "noOfRooms": count[typesOfRoom[i]],
            "roomDetails": [

            ],
            "imageList": [

            ],
            "minimumLengthOfStay": 0,
            "maximumLengthOfStay": 0,
            "ranking": 0,
            "roomFacilities": [

            ],
            "dayTrip": False,
            "shared": False
        }

        addRoomApiRes = s.post(
            addRoomApi, json=addRoomPayload, headers=header)
        print(addRoomApiRes.status_code)
        if addRoomApiRes.status_code == 201:
            print('Add room api status code',
                  addRoomApiRes.status_code, 'for room type ', i+1)

    return addRoomApiRes.status_code
