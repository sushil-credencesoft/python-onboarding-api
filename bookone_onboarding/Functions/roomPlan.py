import requests
from datetime import date, timedelta
import os
from bookone_onboarding import helper
import time
from datetime import datetime


config=helper.read_config()

s=requests.Session()

allRoomIdAndPrices=[]

def minimumPriceFunction(l):
    returnList=[]
    allAmounts=[]
    [allAmounts.append(int(x['amount'])) for x in l]
    allAmounts.sort()

    for x in l:
        if x['amount'] == str(allAmounts[0]):
            returnList.append(x)

    return returnList





def addRoomPlan(allRoomIdList, propertyId, header, roomType, extraChargePerPerson):
    if os.environ['env_variable'] == 'TEST':
        addRoomPlanApi = config['TestApi']['addroomplanapi']
        otaApI = config['TestApi']['otaapi']
    elif os.environ['env_variable'] == 'PRODUCTION':
        addRoomPlanApi = config['ProductionApi']['addroomplanapi']
        otaApI = config['ProductionApi']['otaapi']

    effectiveDate = date.today()
    timeDiff = timedelta(days=30)
    expiryDate = effectiveDate + timeDiff

    count = 1
    for i in range(len(allRoomIdList)):
        planName = roomType[allRoomIdList[i]['type']]['roomPlan']
        roomId = allRoomIdList[i]['id']

        for x in planName:
            code = ''
            for a in allRoomIdList[i]['type'].split():
                code = code + a[0].upper()

            finalCode = code + '-' + str(count)


            payload = {
                "dayOfTheWeekList": [
                    "MONDAY", "TUESDAY", "WEDNESDAY",
                    "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"
                ],
                "status": "Open",
                "maximumLengthOfStay": 999,
                "minimumLengthOfStay": 1,
                "restriction": "None",
                "code": finalCode,
                "name": x,
                "minimumOccupancy": 2,
                "maximumOccupancy": 4,
                "extraChargePerPerson": int(extraChargePerPerson),
                "noOfChildren": 0,
                "extraChargePerChild3To5yrs": 0,
                "extraChargePerChild": 0,
                "effectiveDate": effectiveDate.strftime("%Y-%m-%d"),
                "expiryDate": expiryDate.strftime("%Y-%m-%d"),
                "currencyCode": "INR",
                "amount": int(planName[x]),
                "active": True,
                "propertyId": propertyId,
                "roomTypeId": roomId,
                "roomId": roomId,
                "deviationFromStandardPlan": 50,
                "occupancyBased": False,
                "extraPersonChargeIncluded": False,
                "isApplicableToOta": True
            }

            obj = {
                'roomId': roomId,
                'amount': int(planName[x]),
                'planName': x,
                'planCode': finalCode
            }
            allRoomIdAndPrices.append(obj)

            editedAddRoomPlanApi = (
                addRoomPlanApi
                .replace('{propertyId}', str(propertyId))
                .replace('{individualRoomId}', str(roomId))
            )

            print(f"Calling URL: {editedAddRoomPlanApi}")

            print(editedAddRoomPlanApi, propertyId, roomId)
            print(payload)
            roomPlanApiRes = s.post(
                editedAddRoomPlanApi, json=payload, headers=header)
            roomPlanApiStatusCode = roomPlanApiRes.status_code
            print(roomPlanApiStatusCode)
            if roomPlanApiStatusCode == 201:
                print('Add room plan api status code', roomPlanApiStatusCode, 'for plan ', i + 1)
            count = count + 1

        time.sleep(5)
        count = 1
    

    ######### Below commented code is for adding the OTA plan.Currently it is not in use. ################
    
    # minimumPriceList=minimumPriceFunction(allRoomIdAndPrices)
    
    # header1={
    #     'Authorization': header['Authorization'],
    #     'APP_ID': header['APP_ID']
    # }

    # for m in minimumPriceList:
    #     roomId=m['roomId']
    #     otaPayload={
    #         "bookonePlanCode": str(m['planCode']),
    #         "otaPlanId": str(m['planCode']),
    #         "otaPlanId":"GHC",
    #         "planName": str(m['planName']),
    #         "price": int(m['amount'])
    #         }
        
    #     print(otaPayload)
        
    #     currentOTAapi=otaApI.replace('{roomId}',str(roomId))
    #     print(otaApI)
    #     otaApiCall=s.post(currentOTAapi,json=otaPayload,headers=header1)
    #     print(otaApiCall.status_code)
    #     break
        
    return roomPlanApiStatusCode



