import requests
from datetime import date, timedelta
import os
import logging
from bookone_onboarding import helper

logger = logging.getLogger(__name__)

config = helper.read_config()

s = requests.Session()

FLOOR_MAP = {
    "basement": ("Basement Floor", "BF"),
    "bf": ("Basement Floor", "BF"),
    "ground": ("Ground Floor", "GF"),
    "gf": ("Ground Floor", "GF"),
    "terrace": ("Terrace Floor", "Terrace"),
    "first": ("First", "1st"),
    "1st": ("First", "1st"),
    "second": ("Second", "2nd"),
    "2nd": ("Second", "2nd"),
    "third": ("Third", "3rd"),
    "3rd": ("Third", "3rd"),
    "fourth": ("Fourth", "4th"),
    "4th": ("Fourth", "4th"),
    "fifth": ("Fifth", "5th"),
    "5th": ("Fifth", "5th"),
    "sixth": ("Sixth", "6th"),
    "6th": ("Sixth", "6th"),
    "seventh": ("Seventh", "7th"),
    "7th": ("Seventh", "7th"),
    "eighth": ("Eighth", "8th"),
    "8th": ("Eighth", "8th"),
    "ninth": ("Ninth", "9th"),
    "9th": ("Ninth", "9th"),
    "tenth": ("Tenth", "10th"),
    "10th": ("Tenth", "10th"),
    "eleventh": ("Eleventh", "11th"),
    "11th": ("Eleventh", "11th"),
    "twelfth": ("Twelvth", "12th"),
    "twelvth": ("Twelvth", "12th"),
    "12th": ("Twelvth", "12th"),
    "thirteenth": ("Thirteenth", "13th"),
    "13th": ("Thirteenth", "13th"),
    "fourteenth": ("Fourteenth", "14th"),
    "14th": ("Fourteenth", "14th"),
    "fifteenth": ("Fifteenth", "15th"),
    "15th": ("Fifteenth", "15th"),
    "sixteenth": ("Sixteenth", "16th"),
    "16th": ("Sixteenth", "16th"),
    "seventeenth": ("Seventeenth", "17th"),
    "17th": ("Seventeenth", "17th"),
    "eighteenth": ("Eighteenth", "18th"),
    "18th": ("Eighteenth", "18th"),
    "nineteenth": ("Nineteenth", "19th"),
    "19th": ("Nineteenth", "19th"),
    "twentieth": ("Twentieth", "20th"),
    "20th": ("Twentieth", "20th"),
}


def resolve_floor(floor_raw: str):
    if not floor_raw:
        return "Ground Floor", "GF"

    clean = floor_raw.strip().lower()
    first_word = clean.split()[0] if clean else "ground"

    if clean in FLOOR_MAP:
        return FLOOR_MAP[clean]
    if first_word in FLOOR_MAP:
        return FLOOR_MAP[first_word]

    return floor_raw.strip(), "GF"


def addRoomDetails(allRoomIdList, propertyId, header, roomDetails):

    if os.environ['env_variable'] == 'TEST':
        addRoomDetailsApi = config['TestApi']['addroomdetailsapi'].replace(
            '{propertyId}', str(propertyId))
    elif os.environ['env_variable'] == 'PRODUCTION':
        addRoomDetailsApi = config['ProductionApi']['addroomdetailsapi'].replace(
            '{propertyId}', str(propertyId))

    uniqueList = []

    floors = list(roomDetails.keys())
    sequence_count = 1

    for floor_key in floors:
        floor_name, floor_number = resolve_floor(floor_key)

        room_types_on_floor = list(roomDetails[floor_key].keys())
        for room_type_name in room_types_on_floor:
            roomID = None
            for created_room in allRoomIdList:
                if created_room['type'].strip().lower() == room_type_name.strip().lower():
                    roomID = created_room['id']
                    break

            if roomID is None:
                logger.warning(
                    f"Room type '{room_type_name}' not found in room ID list: {allRoomIdList}"
                )
                continue

            room_number_list = roomDetails[floor_key][room_type_name].get('room numbers', [])
            for room_number in room_number_list:
                payload = {
                    "roomId": roomID,
                    "floorName": floor_name,
                    "floorNumber": floor_number,
                    "available": True,
                    "roomStatus": "VACANT_READY",
                    "roomNumber": str(room_number),
                    "roomSequenceNumber": sequence_count,
                    "noOfBed": "1",
                    "bedType": room_type_name
                }
                sequence_count += 1
                if payload not in uniqueList:
                    uniqueList.append(payload)

    last_status = 200
    for room_payload in uniqueList:
        extractedRoomId = room_payload['roomId']
        apiCall = s.post(
            addRoomDetailsApi.replace('{extractedRoomId}', str(extractedRoomId)),
            headers=header,
            json=room_payload
        )
        print(f"Add room detail for room {room_payload['roomNumber']} status: {apiCall.status_code}")
        last_status = apiCall.status_code

    return last_status
