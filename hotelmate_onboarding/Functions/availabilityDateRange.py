import requests
from datetime import date, timedelta
from hotelmate_onboarding.helper import read_config
import os

config = read_config()

s = requests.Session()


def addAvailabilityByDateRange(allRoomIdList, propertyId, header, roomType, count):

    fromDate = date.today()
    timeSpan = timedelta(days=10)
    # for 1 years
    toDate = fromDate+timeSpan

    if os.environ['env_variable'] == 'TEST':
        addAvailabilityByDate = config['TestApi']['addavailabilitybydate']
    elif os.environ['env_variable'] == 'PRODUCTION':
        addAvailabilityByDate = config['ProductionApi']['addavailabilitybydate']

    for i in range(len(allRoomIdList)):  
        payload = {
            "roomId": allRoomIdList[i]['id'],
            "propertyId": propertyId,
            "price": roomType[allRoomIdList[i]['type']]['roomStandardPrice'],
            "noOfRooms": count[allRoomIdList[i]['type']],
            "fromDate": str(fromDate),
            "toDate": str(toDate)
        }
        print("availability", payload )

        addAvailabilityByDateApiCall = s.post(
            addAvailabilityByDate, headers=header, json=payload)
        
        print('availablility date range status code ',
              addAvailabilityByDateApiCall.status_code, 'for room type', i+1)

    return addAvailabilityByDateApiCall.status_code