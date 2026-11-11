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
from bookone_onboarding.Functions.activateProperty import activateProperty

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ['env_variable'] = os.getenv("SERVER", "PRODUCTION")
logger.info(f" onboarding running in {os.getenv('SERVER', 'PRODUCTION')} environment.")


class BookOneDriverClass:

    def __init__(self, json_data, step_callback=None):
        self.json_data = json_data
        self.step_callback = step_callback
        self.execution_log = []

    def report_step(self, step_num: int, total_steps: int, step_name: str, status: str, details: str = ""):
        entry = {
            "step": f"{step_num:02d}/{total_steps:02d}",
            "step_name": step_name,
            "status": status,
            "details": details,
            "timestamp": time.strftime("%H:%M:%S")
        }
        self.execution_log.append(entry)
        if self.step_callback:
            try:
                if asyncio.iscoroutinefunction(self.step_callback):
                    try:
                        loop = asyncio.get_running_loop()
                        loop.create_task(self.step_callback(entry))
                    except RuntimeError:
                        pass
                else:
                    self.step_callback(entry)
            except Exception as cb_err:
                logger.debug(f"Step callback error: {cb_err}")
        return entry

    async def stage_1(self):
        """Executes Steps 1 to 5: Account creation, user profile, login, short name, property info."""
        x = self.json_data[0] if isinstance(self.json_data, list) else self.json_data
        current_step = (0, 18, "Initialization")
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
            mobileNumber = x['mobile'].strip()
            adminFirstName = x['adminFirstName'].title()
            adminLastName = x['adminLastName'].title()
            googlePlaceId = x.get('googlePlaceId', '')
            gstNumber = x.get('gstNumber') if x.get('gstNumber') else 'N/A'
            roomType = x.get('roomType', {})
            roomDetails = x.get('roomDetails', {})
            extraChargePerPerson = int(x.get('extraPersonCharge', 0) or 0)

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

            # Store on self for subsequent stages
            self.state = {
                "businessName": businessName,
                "businessShortName": businessShortName,
                "password": password,
                "uniqueShortName": uniqueShortName,
                "seoName": seoName,
                "city": city,
                "country": country,
                "locality": locality,
                "postcode": postcode,
                "state": state,
                "streetName": streetName,
                "streetNumber": streetNumber,
                "suburb": suburb,
                "businessType": businessType,
                "businessEmail": businessEmail,
                "mobileNumber": mobileNumber,
                "managerFirstName": x.get('managerFirstName', '').title(),
                "managerLastName": x.get('managerLastName', '').title(),
                "managerContactNumber": x.get('managerContactNo', '').strip(),
                "adminFirstName": adminFirstName,
                "adminLastName": adminLastName,
                "googlePlaceId": googlePlaceId,
                "gstNumber": gstNumber,
                "bankname": x.get('bankName', ''),
                "branchName": x.get('branchName', ''),
                "accountName": x.get('accountName', ''),
                "accountNumber": x.get('accountNumber', ''),
                "swiftcode": x.get('swiftCode', ''),
                "longitude": x.get('Longitude', ''),
                "latitude": x.get('Latitude', ''),
                "roomType": roomType,
                "roomDetails": roomDetails,
                "extraChargePerPerson": extraChargePerPerson,
                "allRoomTypes": allRoomTypes,
                "allFloors": allFloors,
                "count": count,
                "totalNumOfRooms": totalNumOfRooms,
                "pricePerNight": pricePerNight,
                "pricePerWeek": pricePerWeek,
                "pricePerFortNight": pricePerFortNight,
                "pricePerMonth": pricePerMonth,
            }

            # STEP 1: User Sign Up
            current_step = (1, 18, "User Sign Up")
            self.report_step(1, 18, "User Sign Up", "IN_PROGRESS", f"Registering {businessEmail}...")
            signUpData, signUpStatusCode = signUp(businessEmail, password)
            if signUpStatusCode == 226:
                self.report_step(1, 18, "User Sign Up", "FAILED", "Business Email Already exist!")
                return {
                    "businessEmail": businessEmail,
                    "status": "error",
                    "message": "Business Email Already exist!",
                    "failedStep": "User Sign Up",
                    "execution_log": self.execution_log
                }

            userId = signUpData.get('userId')
            self.state["userId"] = userId
            self.report_step(1, 18, "User Sign Up", "SUCCESS", "User account created successfully")
            time.sleep(2)

            # STEP 2: User Profile Setup
            current_step = (2, 18, "User Profile Setup")
            self.report_step(2, 18, "User Profile Setup", "IN_PROGRESS", f"Attaching profile for {adminFirstName} {adminLastName}...")
            updateUser(userId, businessType, businessEmail, password, businessName, mobileNumber, city,
                       suburb, streetName, country, state, postcode, adminFirstName, adminLastName)
            self.report_step(2, 18, "User Profile Setup", "SUCCESS", f"Admin profile linked ({city}, {state})")
            time.sleep(2)

            # STEP 3: Authentication & Login
            current_step = (3, 18, "Authentication & Login")
            self.report_step(3, 18, "Authentication & Login", "IN_PROGRESS", "Authenticating and acquiring property ID...")
            loginApiCall = login(businessEmail, password)
            propertyId = loginApiCall['propertyId']
            token = loginApiCall['token']
            userId = loginApiCall['userId']
            header = {
                'USER_ID': str(userId),
                'Authorization': f'Bearer {token}',
                'APP_ID': 'BOOKONE_WEB_APP'
            }
            self.state["propertyId"] = propertyId
            self.state["userId"] = userId
            self.state["header"] = header
            self.report_step(3, 18, "Authentication & Login", "SUCCESS", f"Property ID assigned: {propertyId}")
            time.sleep(2)

            # STEP 4: Short Name Resolution
            current_step = (4, 18, "Short Name Resolution")
            self.report_step(4, 18, "Short Name Resolution", "IN_PROGRESS", f"Verifying unique short name for '{businessName}'...")
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
                self.report_step(4, 18, "Short Name Resolution", "FAILED", "Duplicate short name. Property deleted.")
                return {
                    "businessEmail": businessEmail,
                    "status": "error",
                    "message": "Duplicate short name. Property deleted.",
                    "failedStep": "Short Name Resolution",
                    "execution_log": self.execution_log
                }

            self.state["finalShortName"] = finalShortName
            self.report_step(4, 18, "Short Name Resolution", "SUCCESS", f"Unique short name: '{finalShortName}'")

            # STEP 5: Property Basic Info
            current_step = (5, 18, "Property Basic Info")
            self.report_step(5, 18, "Property Basic Info", "IN_PROGRESS", "Updating location coordinates and address...")
            updateProperty(propertyId, businessName, finalShortName, businessEmail, mobileNumber,
                           country, postcode, streetNumber, streetName, suburb, city, state, locality,
                           self.state["longitude"], self.state["latitude"], seoName, pricePerNight, pricePerWeek, pricePerFortNight,
                           pricePerMonth, allFloors, allRoomTypes, totalNumOfRooms, googlePlaceId, gstNumber,
                           header)
            self.report_step(5, 18, "Property Basic Info", "SUCCESS", f"Location: {city}, {state}")
            time.sleep(2)

            return {
                "status": "success",
                "stage": 1,
                "propertyId": propertyId,
                "businessName": businessName,
                "businessEmail": businessEmail,
                "shortName": finalShortName,
                "execution_log": self.execution_log,
                "message": f"Stage 1 Complete: Admin account registered. Property ID {propertyId} assigned."
            }

        except Exception as e:
            step_num, total_steps, step_name = current_step if 'current_step' in locals() else (0, 18, "Stage 1")
            self.report_step(step_num, total_steps, step_name, "FAILED", f"Error: {str(e)}")
            logger.error(f"Error in stage 1: {e}", exc_info=True)
            return {
                "businessEmail": x.get('email', 'N/A'),
                "status": "error",
                "message": str(e),
                "failedStep": step_name,
                "execution_log": self.execution_log
            }

    async def stage_2(self):
        """Executes Steps 6 to 10: Subscription, basic setup, room types, room IDs, and room details."""
        if not hasattr(self, "state") or not self.state.get("propertyId"):
            raise ValueError("Stage 1 must be completed before Stage 2.")

        st = self.state
        header = st["header"]
        propertyId = st["propertyId"]
        totalNumOfRooms = st["totalNumOfRooms"]

        try:
            # STEP 6: Subscription Setup
            current_step = (6, 18, "Subscription Setup")
            self.report_step(6, 18, "Subscription Setup", "IN_PROGRESS", "Linking business subscription plan...")
            addSubscription(propertyId, header)
            self.report_step(6, 18, "Subscription Setup", "SUCCESS", "Business Starter subscription activated")
            time.sleep(2)

            # STEP 7: Finish Basic Setup
            current_step = (7, 18, "Finish Basic Setup")
            self.report_step(7, 18, "Finish Basic Setup", "IN_PROGRESS", f"Finalizing property setup ({totalNumOfRooms} total rooms)...")
            finishAPI(header, propertyId, st["businessName"], st["finalShortName"], st["businessEmail"], st["mobileNumber"],
                      st["country"], st["postcode"], st["streetNumber"], st["streetName"], st["suburb"], st["city"], st["state"], st["locality"],
                      st["longitude"], st["latitude"], st["seoName"], st["pricePerNight"], st["pricePerWeek"], st["pricePerFortNight"],
                      st["pricePerMonth"], st["allFloors"], st["allRoomTypes"], totalNumOfRooms)
            self.report_step(7, 18, "Finish Basic Setup", "SUCCESS", f"Initialized {totalNumOfRooms} rooms")
            time.sleep(2)

            # STEP 8: Add Room Types
            current_step = (8, 18, "Add Room Types")
            self.report_step(8, 18, "Add Room Types", "IN_PROGRESS", f"Configuring room categories: {', '.join(st['allRoomTypes'])}...")
            addRoom(propertyId, header, st["roomType"], st["count"])
            self.report_step(8, 18, "Add Room Types", "SUCCESS", f"{len(st['allRoomTypes'])} room categories registered")
            time.sleep(2)

            # STEP 9: Fetch Room IDs
            current_step = (9, 18, "Fetch Room IDs")
            self.report_step(9, 18, "Fetch Room IDs", "IN_PROGRESS", "Retrieving internal room IDs...")
            roomIdList = roomInformation(propertyId, header)
            self.state["roomIdList"] = roomIdList
            self.report_step(9, 18, "Fetch Room IDs", "SUCCESS", f"Retrieved {len(roomIdList)} room keys")
            time.sleep(2)

            # STEP 10: Add Room Details & Floor Mappings
            current_step = (10, 18, "Add Room Details")
            self.report_step(10, 18, "Add Room Details", "IN_PROGRESS", f"Configuring {totalNumOfRooms} room numbers with floor & bed mappings...")
            addRoomDetails(roomIdList, propertyId, header, st["roomDetails"])
            self.report_step(10, 18, "Add Room Details", "SUCCESS", f"{totalNumOfRooms} rooms mapped across {len(st['allFloors'])} floors")
            time.sleep(2)

            return {
                "status": "success",
                "stage": 2,
                "propertyId": propertyId,
                "businessName": st["businessName"],
                "businessEmail": st["businessEmail"],
                "totalRooms": totalNumOfRooms,
                "floors": st["allFloors"],
                "execution_log": self.execution_log,
                "message": f"Stage 2 Complete: {totalNumOfRooms} rooms mapped across {len(st['allFloors'])} floors."
            }

        except Exception as e:
            step_num, total_steps, step_name = current_step if 'current_step' in locals() else (6, 18, "Stage 2")
            self.report_step(step_num, total_steps, step_name, "FAILED", f"Error: {str(e)}")
            logger.error(f"Error in stage 2: {e}", exc_info=True)
            return {
                "businessEmail": st.get("businessEmail", "N/A"),
                "status": "error",
                "message": str(e),
                "failedStep": step_name,
                "execution_log": self.execution_log
            }

    async def stage_3(self):
        """Executes Steps 11 to 18: Rates, room plans, availability calendar, GST, taxes, bank, payment modes, and property activation."""
        if not hasattr(self, "state") or not self.state.get("roomIdList"):
            raise ValueError("Stage 2 must be completed before Stage 3.")


        st = self.state
        header = st["header"]
        propertyId = st["propertyId"]
        roomIdList = st["roomIdList"]

        try:
            # STEP 11: Yearly Rates Generation
            current_step = (11, 18, "Yearly Rates Generation")
            self.report_step(11, 18, "Yearly Rates Generation", "IN_PROGRESS", "Generating 365-day pricing calendar matrix...")
            yearlyGenerateApi(propertyId, header, st["finalShortName"], st["businessEmail"], st["mobileNumber"],
                              st["country"], st["postcode"], st["streetName"], st["suburb"], st["city"], st["state"], st["longitude"], st["latitude"],
                              st["businessName"], st["seoName"], st["pricePerNight"], st["pricePerWeek"], st["pricePerFortNight"],
                              st["pricePerMonth"], st["allFloors"], st["allRoomTypes"], st["totalNumOfRooms"])
            self.report_step(11, 18, "Yearly Rates Generation", "SUCCESS", f"Base rate per night: Rs {st['pricePerNight']}")
            time.sleep(2)

            # STEP 12: Room Plans Setup
            current_step = (12, 18, "Room Plans Setup")
            self.report_step(12, 18, "Room Plans Setup", "IN_PROGRESS", "Setting up room pricing plans & extra charge...")
            addRoomPlan(roomIdList, propertyId, header, st["roomType"], st["extraChargePerPerson"])
            self.report_step(12, 18, "Room Plans Setup", "SUCCESS", f"Plans attached (Extra person charge: Rs {st['extraChargePerPerson']})")
            time.sleep(2)

            # STEP 13: Availability Calendar
            current_step = (13, 18, "Availability Calendar")
            self.report_step(13, 18, "Availability Calendar", "IN_PROGRESS", "Opening room inventory date ranges...")
            addAvailabilityByDateRange(roomIdList, propertyId, header, st["roomType"], st["count"])
            self.report_step(13, 18, "Availability Calendar", "SUCCESS", "Room availability unlocked")
            time.sleep(2)

            # STEP 14: GST Configuration
            current_step = (14, 18, "GST Configuration")
            self.report_step(14, 18, "GST Configuration", "IN_PROGRESS", f"Applying GST number ({st['gstNumber']})...")
            addGST(propertyId, st["businessName"], st["finalShortName"], st["businessEmail"], st["mobileNumber"], st["country"],
                   st["postcode"], st["streetName"], st["suburb"], st["city"], st["state"], st["longitude"], st["latitude"], st["seoName"], st["pricePerNight"],
                   st["pricePerWeek"], st["pricePerFortNight"], st["pricePerMonth"], st["allFloors"], st["allRoomTypes"],
                   st["totalNumOfRooms"], header)
            self.report_step(14, 18, "GST Configuration", "SUCCESS", f"GST details attached: {st['gstNumber']}")
            time.sleep(2)

            # STEP 15: Business Services & Taxes
            current_step = (15, 18, "Business Services & Taxes")
            self.report_step(15, 18, "Business Services & Taxes", "IN_PROGRESS", "Configuring business services, open days & tax slabs...")
            serviceId, serviceStatus = businessServiceApi(propertyId, header)
            openDays(serviceId, header)
            addTaxDetails(serviceId, header, st["country"], st["state"])
            self.report_step(15, 18, "Business Services & Taxes", "SUCCESS", f"Service ID {serviceId} configured with open days & taxes")
            time.sleep(2)

            # STEP 16: Business Profile & Banking
            current_step = (16, 18, "Business Profile & Banking")
            self.report_step(16, 18, "Business Profile & Banking", "IN_PROGRESS", "Linking manager details and bank account...")
            businessProfileUpdate(propertyId, st["businessName"], st["finalShortName"], st["businessEmail"], st["mobileNumber"],
                                  st["country"], st["postcode"], st["streetNumber"], st["streetName"], st["suburb"], st["city"], st["state"],
                                  st["locality"], st["longitude"], st["latitude"], st["seoName"], st["googlePlaceId"], st["gstNumber"],
                                  st["managerFirstName"], st["managerLastName"], st["bankname"], st["branchName"], st["accountName"],
                                  st["accountNumber"], st["swiftcode"], header)
            self.report_step(16, 18, "Business Profile & Banking", "SUCCESS", "Profile and manager details verified")
            time.sleep(2)

            # STEP 17: Mode of Payment
            current_step = (17, 18, "Mode of Payment")
            self.report_step(17, 18, "Mode of Payment", "IN_PROGRESS", "Enabling payment modes (Cash, Card, Online)...")
            modeOfPayment(propertyId, header)
            self.report_step(17, 18, "Mode of Payment", "SUCCESS", "Payment methods enabled")
            time.sleep(2)

            # STEP 18: Property Activation
            current_step = (18, 18, "Property Activation")
            self.report_step(18, 18, "Property Activation", "IN_PROGRESS", "Activating property in BookOne...")
            userId = st.get("userId") or header.get("USER_ID")
            activateProperty(propertyId, userId, header)
            self.report_step(18, 18, "Property Activation", "SUCCESS", "Property activated and live")

            return {
                "status": "success",
                "stage": 3,
                "propertyId": propertyId,
                "businessName": st["businessName"],
                "businessEmail": st["businessEmail"],
                "execution_log": self.execution_log,
                "message": "Onboarding completed successfully"
            }

        except Exception as e:
            step_num, total_steps, step_name = current_step if 'current_step' in locals() else (11, 18, "Stage 3")
            self.report_step(step_num, total_steps, step_name, "FAILED", f"Error: {str(e)}")
            logger.error(f"Error in stage 3: {e}", exc_info=True)
            return {
                "businessEmail": st.get("businessEmail", "N/A"),
                "status": "error",
                "message": str(e),
                "failedStep": step_name,
                "execution_log": self.execution_log
            }

    async def driverFunction(self):
        """Runs all 3 stages sequentially for backward compatibility."""
        try:
            r1 = await self.stage_1()
            if r1.get("status") != "success":
                return [r1]
            r2 = await self.stage_2()
            if r2.get("status") != "success":
                return [r2]
            r3 = await self.stage_3()
            return [r3]
        except Exception as e:
            logger.error(f"Error during onboarding: {e}", exc_info=True)
            return [{
                "businessEmail": self.json_data[0].get("email", "N/A") if isinstance(self.json_data, list) else self.json_data.get("email", "N/A"),
                "status": "error",
                "message": str(e),
                "execution_log": self.execution_log
            }]
