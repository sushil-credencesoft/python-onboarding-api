import json
import requests
import os
from bookone_onboarding import helper
from utils import get_business_subtype

config = helper.read_config()

s = requests.Session()


def addGST(propertyId, businessName, businessShortName, businessEmail, mobileNumber, country, postcode, streetName, suburb, city, state, longitude, latitude, seoName, pricePerNight, pricePerWeek, pricePerFortNight, pricePerMonth, allFloors, allRoomTypes, totalNumOfRooms, header):

    if os.environ['env_variable'] == 'TEST':
        add_GST_Api = config['TestApi']['addgstapi']
    elif os.environ['env_variable'] == 'PRODUCTION':
        add_GST_Api = config['ProductionApi']['addgstapi']

    businessSubType: str = get_business_subtype(businessName)

    actutalPayload = {
        "id": propertyId,
        "name": businessName,
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
        "subscriptionList": [
                {

                    "name": "Booking Management",
                },
            {

                    "name": "Revenue Management",

                    },
            {

                    "name": "Business Setup ",
                    }
        ],
        "verified": False,
        "seoFriendlyName": seoName,
        "imageList": [

        ],
        "taxDetails": [
            {
                "name": "GST",
                "percentage": 5,
                "country": country,
                "state": state,
                "taxableAmount": 100000,
                "taxAmount": 120000,
                "taxSlabsList": [
                        {
                            "minAmount": 1,
                            "maxAmount": 1000,
                            "percentage": 5
                        },
                    {
                            "minAmount": 1001,
                            "maxAmount": 7500,
                            "percentage": 5
                        },
                    {
                            "minAmount": 7501,
                            "maxAmount": 1000000,
                            "percentage": 18
                        }
                ]
            }
        ],
        "socialMediaLinks": [

        ],
        "noOfBookOneReview": 0,
        "pointOfSaleList": [

        ],
        "businessSubtype": businessSubType,
        "propertyServicesList": [

        ],
        "nearbyAttractions": [

        ],
        "propertyInvoicePrintHeader": False,
        "featuredBusiness": False
    }

    apiCall = s.post(add_GST_Api, headers=header, json=actutalPayload)

    addGSTstatusCode = apiCall.status_code
    print('add GST status ', addGSTstatusCode)

    return addGSTstatusCode
