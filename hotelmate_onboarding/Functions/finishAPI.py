import json
import requests
import os
from hotelmate_onboarding.helper import read_config

config = read_config()

s = requests.Session()


def finishAPI(header, propertyId, businessName, businessShortName, businessEmail, mobileNumber, country, postcode, streetNumber, streetName, suburb, city, state, locality, longitude, latitude, seoName, pricePerNight, pricePerWeek, pricePerFortNight, pricePerMonth, allFloors, allRoomTypes, totalNumOfRooms):

    if os.environ['env_variable'] == 'TEST':
        updatePropertyApi = config['TestApi']['updateproperty'].replace(
            '{propertyId}', str(propertyId))
    elif os.environ['env_variable'] == 'PRODUCTION':
        updatePropertyApi = config['ProductionApi']['updateproperty'].replace(
            '{propertyId}', str(propertyId))

    payload = {
        "id": propertyId,
        "name": businessName,
        "shortName": businessShortName,
        "email": businessEmail,
        "mobile": mobileNumber,
        "managerFirstName": '',
        "managerLastName": '',
        "managerContactNo": mobileNumber,
        "managerEmailAddress": businessEmail,
        "address": {
            "country": country,
            "postcode": postcode,
            "streetNumber": streetNumber,
            "streetName": streetName,
            "suburb": suburb,
            "city": city,
            "state": state,
            "locality": locality,
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
        "subscriptionList": [
            {
                "name": "Booking Management",
            },
            {
                "name": "Revenue Management",

            },
            {
                "name": "Business Setup",
            }
        ],
        "verified": False,
        "seoFriendlyName": seoName,
        "imageList": [

        ],
        "taxDetails": [

        ],
        "socialMediaLinks": [

        ],
        "noOfBookOneReview": 0,
        "pointOfSaleList": [

        ],
        "businessSubtype": "Hotels",
        "propertyServicesList": [

        ],
        "nearbyAttractions": [

        ],
        "propertyInvoicePrintHeader": False,
        "featuredBusiness": False
    }

    apiCall = s.post(updatePropertyApi, headers=header, json=payload)

    updatePropertStatusCode = apiCall.status_code
    print('finish api status ', updatePropertStatusCode)

    return updatePropertStatusCode