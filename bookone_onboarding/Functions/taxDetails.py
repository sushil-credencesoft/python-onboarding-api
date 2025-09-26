import requests
import os
from bookone_onboarding import helper
import json

config = helper.read_config()

s = requests.Session()


def addTaxDetails(serviceId, header, country, state):

    if os.environ['env_variable'] == 'TEST':
        taxDetailsApi = config['TestApi']['taxdetailsapi'].replace(
            '{serviceID}', str(serviceId))
    elif os.environ['env_variable'] == 'PRODUCTION':
        taxDetailsApi = config['ProductionApi']['taxdetailsapi'].replace(
            '{serviceID}', str(serviceId))

    payload = [
        {
            "name": "CGST",
            "percentage": 6,
            "country": country,
            "state": state,
            "taxableAmount": 10000000,
            "taxAmount": 600000,
            "taxSlabsList": [
                    {
                        "minAmount": 1,
                        "maxAmount": 1000,
                        "percentage": 6
                    },
                {
                        "minAmount": 1001,
                        "maxAmount": 7500,
                        "percentage": 6
                        },
                {
                        "minAmount": 7501,
                        "maxAmount": 10000000,
                        "percentage": 9
                        }
            ]
        },
        {
            "name": "SGST",
            "percentage": 6,
            "country": country,
            "state": state,
            "taxableAmount": 10000000,
            "taxAmount": 600000,
            "taxSlabsList": [
                    {
                        "minAmount": 1,
                        "maxAmount": 1000,
                        "percentage": 6
                    },
                {
                        "minAmount": 1001,
                        "maxAmount": 7500,
                        "percentage": 6
                        },
                {
                        "minAmount": 7501,
                        "maxAmount": 10000000,
                        "percentage": 9
                        }
            ]
        },
        {
            "name": "IGST",
            "percentage": 6,
            "country": country,
            "state": state,
            "taxableAmount": 10000000,
            "taxAmount": 60000,
            "taxSlabsList": [
                    {
                        "minAmount": 1,
                        "maxAmount": 1000,
                        "percentage": 6
                    },
                {
                        "minAmount": 1001,
                        "maxAmount": 7500,
                        "percentage": 6
                        },
                {
                        "minAmount": 7501,
                        "maxAmount": 10000000,
                        "percentage": 9
                        }
            ]
        }
    ]

    taxDetailsApiCall = s.post(taxDetailsApi, headers=header, json=payload)
    print('tax details api status code ', taxDetailsApiCall.status_code)

    return taxDetailsApiCall.status_code
