import requests
import os
from bookone_onboarding import helper

config = helper.read_config()

s = requests.Session()

SUBSCRIPTION_LIST = [
    "Analytics",
    "Booking Engine",
    "Booking Management",
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
    "Host Email Notification",
    "Inventory Management Access",
    "Mobile App",
    "Rates Management Access",
    "Revenue Management",
    "Room Management",
    "Service Management",
    "THM Subscription"
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
