import requests
import os
from hotelmate_onboarding.helper import read_config
from utils import get_business_subtype


config = read_config()

s = requests.Session()


def yearlyGenerateApi(propertyId, header, businessShortName, businessEmail, mobileNumber, country, postcode, streetName, suburb, city, state, longitude, latitude, bussinessName, seoName, pricePerNight, pricePerWeek, pricePerFortNight, pricePerMonth, allFloors, allRoomTypes, totalNumOfRooms):

    if os.environ['env_variable'] == 'TEST':
        yearlyRatesApi = config['TestApi']['yearlygenerateratesapi'].replace(
            '{propertyId}', str(propertyId))
    elif os.environ['env_variable'] == 'PRODUCTION':
        yearlyRatesApi = config['ProductionApi']['yearlygenerateratesapi'].replace(
            '{propertyId}', str(propertyId))


    yearlyRatesPayload = {
        "id": propertyId,
        "name": bussinessName,
        "shortName": businessShortName,
        "email": businessEmail,
        "mobile": mobileNumber,
        "managerFirstName": "",
        "managerLastName": "",
        "managerContactNo": mobileNumber,
        "managerEmailAddress": businessEmail,
        "address": {
            "country": country,
            "postcode": postcode,
            "streetNumber": "",
            "streetName": streetName,
            "suburb": suburb,
            "city": city,
            "state": state,
            "locality": "",
            "addressLine1": None,
            "addressLine2": None
        },
        "propertyStatus": "COMPLETED",
        "gstNumber": "123456789",
        "pricePerNight": pricePerNight,
        "pricePerWeek": pricePerWeek,
        "priceFortNight": pricePerFortNight,
        "priceMonthly": pricePerMonth,
        "minimumOccupancy": 2,
        "maximumOccupancy": 4,
        "localCurrency": "INR",
        "noOfFloor": len(allFloors),
        "noOfRoomType": len(allRoomTypes),
        "numberOfRooms": totalNumOfRooms,
        "organisationId": 1,
        "longitude": longitude,
        "latitude": latitude,
        "businessType": "Accommodation",
        "plan": "Business Premium",
        "verified": False,
        "seoFriendlyName": seoName,
        "subscriptionList":[],
        "imageList": [
        ],
        "taxDetails": [
        ],
        "socialMediaLinks": [
        ],
        "noOfBookOneReview": 0,
        "pointOfSaleList": [
        ],
        "businessSubtype": get_business_subtype(bussinessName),
        "propertyServicesList": [
        ],
        "nearbyAttractions": [
        ],
        "propertyInvoicePrintHeader": False,
        "featuredBusiness": False
    }

    generateYearlyRates = s.post(
        yearlyRatesApi, json=yearlyRatesPayload, headers=header)
    yearlyStatusCode = generateYearlyRates.status_code
    print(yearlyStatusCode)
    if yearlyStatusCode == 200:
        print('Generate yearly rates status code ',
              generateYearlyRates.status_code)

    return yearlyStatusCode
