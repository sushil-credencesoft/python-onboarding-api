import requests
import os
from hotelmate_onboarding.helper import read_config
import json

config = read_config()

s = requests.Session()


def addTaxDetails(serviceId, header, country, state):

    if os.environ['env_variable'] == 'TEST':
        taxDetailsApi = config['TestApi']['taxdetailsapi'].replace(
            '{businessServiceId}', str(serviceId))
        print("addGst:", taxDetailsApi)
    elif os.environ['env_variable'] == 'PRODUCTION':
        taxDetailsApi = config['ProductionApi']['taxdetailsapi'].replace(
            '{businessServiceId}', str(serviceId))
        print("addGst:", taxDetailsApi)

    payload = [
        {
            "name": "CGST",
            "percentage": 2.5,
            "country": country,
            "state": state,
            "taxableAmount": 1000000,
            "taxAmount": 600000,
            "taxSlabsList": [
                    {
                        "minAmount": 1,
                        "maxAmount": 1000,
                        "percentage": 2.5
                    },
                {
                        "minAmount": 1001,
                        "maxAmount": 7500,
                        "percentage": 2.5
                        },
                {
                        "minAmount": 7501,
                        "maxAmount": 1000000,
                        "percentage": 9
                        }
            ]
        },
        {
            "name": "SGST",
            "percentage": 2.5,
            "country": country,
            "state": state,
            "taxableAmount": 1000000,
            "taxAmount": 600000,
            "taxSlabsList": [
                    {
                        "minAmount": 1,
                        "maxAmount": 1000,
                        "percentage": 2.5
                    },
                {
                        "minAmount": 1001,
                        "maxAmount": 7500,
                        "percentage": 2.5
                        },
                {
                        "minAmount": 7501,
                        "maxAmount": 1000000,
                        "percentage": 9
                        }
            ]
        },
        {
            "name": "IGST",
            "percentage": 2.5,
            "country": country,
            "state": state,
            "taxableAmount": 1000000,
            "taxAmount": 60000,
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
    ]

    taxDetailsApiCall = s.post(taxDetailsApi, headers=header, json=payload)
    print('tax details api status code ', taxDetailsApiCall.status_code)

    return taxDetailsApiCall.status_code
