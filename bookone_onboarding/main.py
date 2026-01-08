import time
import json
import os
import asyncio
import logging


from bookone_onboarding.Functions.signUp import signUp
from bookone_onboarding.Functions.login import login
from bookone_onboarding.Functions.updateUser import updateUser
from bookone_onboarding.Functions.addSubscription import addSubscription
from bookone_onboarding.Functions.addRoom import addRoom
from bookone_onboarding.Functions.roomInfo import roomInformation
from bookone_onboarding.Functions.roomPlan import addRoomPlan
from bookone_onboarding.Functions.availabilityDateRange import addAvailabilityByDateRange
from bookone_onboarding.Functions.yearlyGenerate import yearlyGenerateApi
from bookone_onboarding.Functions.businessService import businessServiceApi
from bookone_onboarding.Functions.updateProperty import updateProperty
from bookone_onboarding.Functions.finishAPI import finishAPI
from bookone_onboarding.Functions.roomDetails import addRoomDetails
from bookone_onboarding.Functions.addGST import addGST
from bookone_onboarding.Functions.openDays import openDays
from bookone_onboarding.Functions.taxDetails import addTaxDetails
from bookone_onboarding.Functions.businessProfileModule import businessProfileUpdate
from bookone_onboarding.Functions.modeOfPayment import modeOfPayment
from bookone_onboarding.Functions.checkBusinessShortName import checkBusinessShortName
from bookone_onboarding.Functions.deleteUser_Property import delet_user_and_property
import json
import asyncio
import os
# from bookone_onboarding.main import BookOneDriverClass  # adjust import if needed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ['env_variable'] = os.getenv("SERVER", "PRODUCTION")
logger.info(f" onboarding running in {os.getenv("SERVER", "PRODUCTION")} environment.")


class BookOneDriverClass:

    def __init__(self, json_data):
        self.json_data = json_data

    async def driverFunction(self):
        results = []

        for x in self.json_data:
            try:
                logger.info("Initializing business data extraction...")

                businessName = x.get('BusinessName', '').title()
                if not businessName:
                    raise ValueError("Missing BusinessName")

                businessShortName = ''.join([i[0].upper() for i in businessName.split()])
                password = os.getenv("DEFAULT_PASSWORD", "Pass@1234")

                # Generate unique short names
                uniqueShortName = set()
                position = 1
                for word in businessName.split():
                    prefix = businessShortName[0:position]
                    suffix = businessShortName[position:]
                    for char in word[1:]:
                        finalShortName = (prefix + char + suffix).upper()
                        uniqueShortName.add(finalShortName)
                    position += 1

                seoName = '-'.join(businessName.split()).replace(',', '')

                # Optional fields
                businessUrl = x.get('BusinessUrl', '')
                website = x.get('website', '')
                businessSource = x.get('source', '')
                businessStatus = x.get('status', '')
                roomType = x.get('roomType', {})
                roomPlan = x.get('Room Plan', '')
                longitude = x.get('Longitude', '')
                latitude = x.get('Latitude', '')
                images = x.get('images', [])

                # Required fields
                city = x['city']
                country = x['country']
                locality = x['locality']
                postcode = x['postcode']
                state = x['state']
                streetName = x['streetName']
                streetNumber = x['streetNumber']
                suburb = x['subUrb']
                businessType = x['BusinessType']
                businessEmail = x['email']
                managerContactNumber = x['managerContactNo'].strip()
                mobileNumber = x['mobile'].strip()
                managerFirstName = x['managerFirstName'].title()
                managerLastName = x['managerLastName'].title()
                googlePlaceId = x['googlePlaceId']
                status = x['status']
                source = x['source']
                bankname = x['bankName']
                branchName = x['branchName']
                accountName = x['accountName']
                accountNumber = x['accountNumber']
                swiftcode = x['swiftCode']
                gstNumber = x['gstNumber'] if x.get('gstNumber') else 'N/A'
                roomDetails = x['roomDetails']
                extraChargePerPerson = int(x['extraPersonCharge'])
                adminFirstName = x['adminFirstName'].title()
                adminLastName = x['adminLastName'].title()

                allRoomTypes = list(roomType.keys())
                allFloors = list(roomDetails.keys())

                # Count rooms
                count = {}
                for floor in allFloors:
                    for room in allRoomTypes:
                        try:
                            count[room] = count.get(room, 0) + len(roomDetails[floor][room]['room numbers'])
                        except Exception as e:
                            logger.warning(f"Room counting error: {e}")

                totalRoomPrice = sum(int(roomType[c]['roomStandardPrice']) * count[c] for c in count)
                totalNumOfRooms = sum(count.values())
                pricePerNight = totalRoomPrice + (totalNumOfRooms * extraChargePerPerson)
                pricePerWeek = pricePerNight * 7
                pricePerFortNight = pricePerNight * 15
                pricePerMonth = pricePerNight * 30

                logger.info(f"Signing up user with email {businessEmail}...")
                signUpData, signUpStatusCode = signUp(businessEmail, password)
                if signUpStatusCode == 226:
                    logger.info(f"{signUpData} Aborting...")
                    logger.warning("Business Email Already exist!")
                    return "Business Email Already exist!"

                userId = signUpData['userId']
                logger.info(f"User created successfully: {userId}")
                time.sleep(2)

                updateUser(userId, businessType, businessEmail, password, businessName, mobileNumber, city,
                           suburb, streetName, country, state, postcode, adminFirstName, adminLastName)
                time.sleep(2)

                logger.info("Logging in...")
                loginApiCall = login(businessEmail, password)
                propertyId = loginApiCall['propertyId']
                token = loginApiCall['token']
                userId = loginApiCall['userId']
                apiToken = f'Bearer {token}'
                header = {
                    'USER_ID': str(userId),
                    'Authorization': apiToken,
                    'APP_ID': 'BOOKONE_WEB_APP'
                }
                logger.info(f"Login successful. Property ID: {propertyId}")
                time.sleep(2)

                logger.info("Generating short name...")
                finalShortName = ''
                if checkBusinessShortName(header, businessShortName) == "false":
                    finalShortName = businessShortName
                else:
                    for u in uniqueShortName:
                        if checkBusinessShortName(header, u) == "false":
                            finalShortName = u
                            break

                if finalShortName == '':
                    delet_user_and_property(header, propertyId)
                    logger.info("Duplicate short name. Property deleted.")
                    return

                logger.info("Updating property info...")
                updateProperty(propertyId, businessName, finalShortName, businessEmail, mobileNumber,
                               country, postcode, streetNumber, streetName, suburb, city, state, locality,
                               longitude, latitude, seoName, pricePerNight, pricePerWeek, pricePerFortNight,
                               pricePerMonth, allFloors, allRoomTypes, totalNumOfRooms, googlePlaceId, gstNumber,
                               header)
                time.sleep(2)

                logger.info("Adding subscription...")
                addSubscription(propertyId, header)
                time.sleep(2)

                logger.info("Finishing basic setup...")
                finishAPI(header, propertyId, businessName, finalShortName, businessEmail, mobileNumber,
                          country, postcode, streetNumber, streetName, suburb, city, state, locality,
                          longitude, latitude, seoName, pricePerNight, pricePerWeek, pricePerFortNight,
                          pricePerMonth, allFloors, allRoomTypes, totalNumOfRooms)
                time.sleep(2)

                logger.info("Adding room types...")
                addRoom(propertyId, header, roomType, count)
                time.sleep(2)

                logger.info("Fetching room IDs...")
                roomIdList = roomInformation(propertyId, header)
                logger.info(f"Room IDs: {roomIdList}")
                time.sleep(2)

                logger.info("Adding room details...")
                addRoomDetails(roomIdList, propertyId, header, roomDetails)
                time.sleep(2)

                logger.info("Generating yearly API data...")
                yearlyGenerateApi(propertyId, header, finalShortName, businessEmail, mobileNumber,
                                  country, postcode, streetName, suburb, city, state, longitude, latitude,
                                  businessName, seoName, pricePerNight, pricePerWeek, pricePerFortNight,
                                  pricePerMonth, allFloors, allRoomTypes, totalNumOfRooms)
                time.sleep(2)

                logger.info("Adding room plan...")
                addRoomPlan(roomIdList, propertyId, header, roomType, extraChargePerPerson)
                time.sleep(2)

                logger.info("Adding availability by date range...")
                addAvailabilityByDateRange(roomIdList, propertyId, header, roomType, count)
                time.sleep(2)

                logger.info("Adding GST info...")
                addGST(propertyId, businessName, finalShortName, businessEmail, mobileNumber, country,
                       postcode, streetName, suburb, city, state, longitude, latitude, seoName, pricePerNight,
                       pricePerWeek, pricePerFortNight, pricePerMonth, allFloors, allRoomTypes,
                       totalNumOfRooms, header)
                time.sleep(2)

                logger.info("Setting up business services...")
                serviceId, serviceStatus = businessServiceApi(propertyId, header)
                openDays(serviceId, header)
                addTaxDetails(serviceId, header, country, state)
                time.sleep(2)

                logger.info("Updating business profile...")
                businessProfileUpdate(propertyId, businessName, finalShortName, businessEmail, mobileNumber,
                                      country, postcode, streetNumber, streetName, suburb, city, state,
                                      locality, longitude, latitude, seoName, googlePlaceId, gstNumber,
                                      managerFirstName, managerLastName, bankname, branchName, accountName,
                                      accountNumber, swiftcode, header)
                time.sleep(2)

                logger.info("Adding modes of payment...")
                modeOfPayment(propertyId, header)

                results.append({
                    "businessEmail": businessEmail,
                    "status": "success",
                    "message": "Property onboarded successfully"
                })

            except Exception as e:
                logger.error(f"Error onboarding business {x.get('email')}: {e}", exc_info=True)
                results.append({
                    "businessEmail": x.get('email', 'N/A'),
                    "status": "error",
                    "message": str(e)
                })

        return results


