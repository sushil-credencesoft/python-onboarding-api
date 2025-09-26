import json
import requests
import os
from bookone_onboarding import helper
from utils import get_business_subtype

config = helper.read_config()

s = requests.Session()



def businessProfileUpdate(propertyId, businessName, businessShortName, businessEmail, mobileNumber, country, postcode, streetNumber, streetName, suburb, city, state, locality, longitude, latitude, seoName, googlePlaceId, gstNumber, managerFirstName, managerLastName, bankname,
                          branchName, accountName, accountNumber, swiftcode, header):

    if os.environ['env_variable'] == 'TEST':
        businessProfileUpdateApi = config['TestApi']['businessprofileupdateapi']
    elif os.environ['env_variable'] == 'PRODUCTION':
        businessProfileUpdateApi = config['ProductionApi']['businessprofileupdateapi']

    businessSubType: str = get_business_subtype(businessName)

    payload = {
        "id": propertyId,
        "name": businessName,
        "shortName": businessShortName,
        "email": businessEmail,
        "slogan": "",
        "mobile": mobileNumber,
        "whatsApp": mobileNumber,
        "managerFirstName": managerFirstName,
        "managerLastName": managerLastName,
        "managerContactNo": "",
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
        "gstNumber": gstNumber,
        "udyamRegistrationNumber": "",
        "logoUrl": "",
        "localCurrency": "INR",
        "placeId": googlePlaceId,
        "website": "",
        "organisationId": 1,
        "longitude": longitude,
        "latitude": latitude,
        "businessType": "Accommodation",
        "businessDescription": "<p>Welcome to our property.</p>",
        "plan": "Business Premium",
        "pointOfSaleList": [{
                        "propertyId": propertyId,
                        "counterName": "Counter 1",
                        "counterNumber": "Front Desk",
                        "operatorName": [
                            'Morning shift',
                            'Afternoon shift',
                            'Evening shift',
                        ]
        }],
        "bankAccount": {
            "bankName": bankname,
            "branchName": branchName,
            "accountName": accountName,
            "accountNumber": accountNumber,
            "swiftCode": swiftcode
        },
        "verified": False,
        "seoFriendlyName": seoName,

        "imageList": [
        ],"taxDetails": [
            {
                "name": "GST",
                "percentage": 5,
                "country": country,
                "state": state,
                "taxableAmount": 10000000,
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
        "detailedView": {
            "yearWiseVisits": {
                "2022": {
                    "DECEMBER": 1,
                    "NOVEMBER": 6
                },
                "2023": {
                    "APRIL": 15,
                    "MARCH": 37,
                    "JANUARY": 9,
                    "FEBRUARY": 2
                }
            },
            "totalNumberOfVisits": 70
        },
        "noOfBookOneReview": 0,
        "sacCode": "",
        "fssaiRegNumber": "",
        "businessSubtype": businessSubType,
        "propertyServicesList": [
            {

                "organisationId": 1,
                "name": "Breakfast",

                "businessType": "Accommodation",
                "serviceType": "Food",

                "applicableToChild": False,
                "applicableToAdult": False
            },
            {

                "organisationId": 1,
                "name": "Lunch  ",

                "businessType": "Accommodation",
                "serviceType": "Food",

                "applicableToChild": False,
                "applicableToAdult": False
            },
            {

                "organisationId": 1,
                "name": "Dinner",

                "businessType": "Accommodation",
                "serviceType": "Food",

                "applicableToChild": False,
                "applicableToAdult": False
            },
            {

                "organisationId": 1,
                "name": "Tea-Coffee",

                "businessType": "Accommodation",
                "serviceType": "Beverages",

                "applicableToChild": False,
                "applicableToAdult": False
            },
            {

                "organisationId": 1,
                "name": " Laundry ",

                "businessType": "Accommodation",
                "serviceType": "Activity",

                "applicableToChild": False,
                "applicableToAdult": False
            },
            {

                "organisationId": 1,
                "name": "Late Check-Out ",

                "businessType": "Accommodation",
                "serviceType": "Express Checkout",
                "afterTaxAmount": 0,
                "beforeTaxAmount": 0,
                "taxAmount": 0,
                "taxPercentage": 0,
                "servicePrice": 0,
                "applicableToChild": False,
                "applicableToAdult": True
            },
            {

                "organisationId": 1,
                "name": "Pick Up",

                "businessType": "Accommodation",
                "serviceType": "Transport",

                "applicableToChild": False,
                "applicableToAdult": False
            },
            {

                "organisationId": 1,
                "name": "Drop Off",

                "businessType": "Accommodation",
                "serviceType": "Transport",

                "applicableToChild": False,
                "applicableToAdult": False
            },
            {

                "organisationId": 1,
                "name": " Spa",

                "businessType": "Accommodation",
                "serviceType": "Spa",

                "applicableToChild": False,
                "applicableToAdult": False
            },
            {

                "organisationId": 1,
                "name": "Food Charge",
                "businessType": "Accommodation",
                "serviceType": "Food",

                "applicableToChild": False,
                "applicableToAdult": False
            },
            {

                "organisationId": 1,
                "name": "Extra Bed",

                "businessType": "Accommodation",
                "serviceType": "Extra Bed",

                "applicableToChild": False,
                "applicableToAdult": False
            },
            {

                "organisationId": 1,
                "name": "Hi-Tea",

                "businessType": "Accommodation",
                "serviceType": "Beverages",

                "applicableToChild": False,
                "applicableToAdult": False
            },
            {

                "organisationId": 1,
                "name": "BreakFast, Lunch, Dinner",

                "businessType": "Accommodation",
                "serviceType": "Food",

                "applicableToChild": False,
                "applicableToAdult": False
            },
            {

                "organisationId": 1,
                "name": "adult meal",

                "businessType": "Accommodation",
                "serviceType": "meal",

                "applicableToChild": False,
                "applicableToAdult": False
            },
            {

                "organisationId": 1,
                "name": "Kid meal",

                "businessType": "Accommodation",
                "serviceType": "meal",

                "applicableToChild": False,
                "applicableToAdult": False
            },
            {

                "organisationId": 1,
                "name": "Pet Service",

                "businessType": "Accommodation",
                "serviceType": "Pet Charge",

                "applicableToChild": False,
                "applicableToAdult": False
            }
        ],
        "nearbyAttractions": [

        ],
        "propertyInvoicePrintHeader": True,
        "featuredBusiness": False
    }

    apiCall = s.post(businessProfileUpdateApi, headers=header, json=payload)

    businessProfileUpdateStatusCode = apiCall.status_code
    print('business profile update status code',
          businessProfileUpdateStatusCode)

    return businessProfileUpdateStatusCode
