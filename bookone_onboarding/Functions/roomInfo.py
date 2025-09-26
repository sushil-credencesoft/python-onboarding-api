import json
import requests
import os
from bookone_onboarding import helper

config=helper.read_config()

s=requests.Session()

def roomInformation(propertyId,header):

    if os.environ['env_variable'] == 'TEST':
        getRoomDetailsApi=config['TestApi']['getroomdetailsapi'].replace('{propertyId}',str(propertyId))
    elif os.environ['env_variable'] == 'PRODUCTION':
        getRoomDetailsApi=config['ProductionApi']['getroomdetailsapi'].replace('{propertyId}',str(propertyId))

    getRoomDetailsApiCall = s.get(getRoomDetailsApi, headers=header)
    getRoomDetailsApiStatusCode = getRoomDetailsApiCall.status_code
    print(getRoomDetailsApiStatusCode)
    if getRoomDetailsApiStatusCode == 200:
        print('FETCHED ROOM DETAILS.')
    
    roomData = json.loads(getRoomDetailsApiCall.content)
    roomIdList = []
    for i in range(0, len(roomData)):
        roomID=roomData[i]['id']
        roomType=roomData[i]['name']
        obj={
            "id":roomID,
            'type':roomType.strip()
        }
        roomIdList.append(obj)

    return roomIdList