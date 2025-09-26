import json
import requests
import os
from hotelmate_onboarding.helper import read_config

config = read_config()

s = requests.Session()


def modeOfPayment(propertyId, header):
    if os.environ['env_variable'] == 'TEST':
        modeOfPaymentApi = config['TestApi']['modeofpaymentapi']
    elif os.environ['env_variable'] == 'PRODUCTION':
        modeOfPaymentApi = config['ProductionApi']['modeofpaymentapi']

    allModesOfPayment = [
        'Prepaid',
        'Payment Terminal',
        'Wallet',
        'Cheque',
        'Demand Draft',
        'Bill To Company',
        'UPI',
        'Bill To Room',
        'Pay Pal',
        'Multi Mode Payment',
        'Paytm',
        'PhonePe',
        'Google Pay',
        'Amazon Pay',
        'BharatPe',
        'Post Pay',
        'OYO Paid',
        'OTA Paid',
        'Fab Paid',
        'Petty Cash'
    ]

    for mode in allModesOfPayment:
        payload = {
            "businessType": "All",
            "isPaid": False,
            "organizationId": 1,
            "paymentMode": mode,
            "name": mode,
            "propertyId": propertyId
        }

        apiCall = s.post(modeOfPaymentApi, headers=header, json=payload)

        modesOfPaymentApiCallStatusCode = apiCall.status_code
        print('modes of payment status code', modesOfPaymentApiCallStatusCode)

    return modesOfPaymentApiCallStatusCode
