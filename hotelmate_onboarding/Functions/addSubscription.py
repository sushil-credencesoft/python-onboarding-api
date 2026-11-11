import requests
import os
from hotelmate_onboarding.helper import read_config

config = read_config()

s = requests.Session()

SUBSCRIPTION_LIST = [
    "Booking Engine",
    "Bookone channel manager",
    "BookOne Halo",
    "BookOne Subscription",
    "Business Setup",
    "Channel Management",
    "Guest Cancel Email Notification",
    "Guest Checkin Email Notification",
    "Guest Checkout Email Notification",
    "Guest Confirm Email Notification",
    "Guest Management",
    "Host Email Notification"
]


def addSubscription(propertyId, header):

    if os.environ['env_variable'] == 'TEST':
        addSubscriptionApi = config['TestApi']['addsubscriptionapi'].replace('{propertyId}', str(propertyId))
    elif os.environ['env_variable'] == 'PRODUCTION':
        addSubscriptionApi = config['ProductionApi']['addsubscriptionapi'].replace('{propertyId}', str(propertyId))

    subscriptionList = SUBSCRIPTION_LIST

    for subscription in subscriptionList:
        suscriptionData = {
            "name": subscription,
            "propertyId": propertyId,
            "organisationId": "1",
            "subscriptionType": "MONTHLY",
            "discountAmount": 0,
            "monthlyAmount": 100,
            "annualAmount": 1200
        }

        addSubscriptionApiRes = s.post(
            addSubscriptionApi, headers=header, json=suscriptionData)
        subscriptionStatusCode = addSubscriptionApiRes.status_code
        if subscriptionStatusCode == 200:
            print('Subscription add api status code', subscriptionStatusCode)

    return subscriptionStatusCode
