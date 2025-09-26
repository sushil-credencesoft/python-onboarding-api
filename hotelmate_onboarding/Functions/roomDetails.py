import requests
from datetime import date, timedelta
import os
from hotelmate_onboarding.helper import read_config

config = read_config()

s = requests.Session()


def addRoomDetails(allRoomIdList, propertyId, header, roomDetails):

    if os.environ['env_variable'] == 'TEST':
        addRoomDetailsApi = config['TestApi']['addroomdetailsapi'].replace(
            '{propertyId}', str(propertyId))
    elif os.environ['env_variable'] == 'PRODUCTION':
        addRoomDetailsApi = config['ProductionApi']['addroomdetailsapi'].replace(
            '{propertyId}', str(propertyId))

    mapDict = {
        'Basement': 'BF',
        'Ground': 'GF',
        'First': '1st',
        'Second': '2nd',
        'Third': '3rd',
        'Fourth': '4th',
        'Fifth': '5th',
        'Sixth': '6th',
        'Seventh': '7th',
        'Eighth': '8th',
        'Ninth': '9th',
        'Tenth': '10th'
    }

    uniqueList = []

    floors = list(roomDetails.keys())
    sequence_count=1
    for x in floors:
        floorKeys = list(roomDetails[x].keys())
        for y in floorKeys:
            for z in allRoomIdList:
                if z['type'] == y:
                    roomID = z['id']
                    break
            roomNumberList = roomDetails[x][y]['room numbers']
            for r in roomNumberList:
                payload = {
                    "roomNumber": str(r),
                    "roomSequenceNumber": sequence_count,
                    "noOfBed": 1,
                    "bedType": "King Size",
                    "floorName": x.split()[0],
                    "floorNumber": mapDict[x.split()[0]],
                    "available": True,
                    "roomId": roomID,
                    "roomStatus": "VACANT_READY"
                }
                
                sequence_count+=1
                if payload not in uniqueList:
                    uniqueList.append(payload)
    
                
    for x in uniqueList:
        extractedRoomId = x['roomId']
        api = addRoomDetailsApi.replace('{roomId}',str(extractedRoomId))
        print(extractedRoomId,api)
        apiCall = s.post(api, headers=header, json=x)
        print(apiCall.status_code)

    return apiCall.status_code