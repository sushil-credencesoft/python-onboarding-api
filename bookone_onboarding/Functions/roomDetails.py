import requests
from datetime import date, timedelta
import os
from bookone_onboarding import helper

config = helper.read_config()

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
        'Tenth': '10th',
        'Eleventh': '11th',
        'Twelfth': '12th',
        'Thirteenth': '13th',
        'Fourteenth': '14th',
        'Fifteenth': '15th',
        'Sixteenth': '16th',
        'Seventeenth': '17th',
        'Eighteenth': '18th',
        'Nineteenth': '19th',
        'Twentieth': '20th'
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

        apiCall = s.post(addRoomDetailsApi.replace(
            '{extractedRoomId}', str(extractedRoomId)), headers=header, json=x)
        print(apiCall.status_code)

    return apiCall.status_code
