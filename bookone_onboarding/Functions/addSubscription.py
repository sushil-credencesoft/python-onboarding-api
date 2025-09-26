import requests
import os
from bookone_onboarding import helper

config=helper.read_config()

s=requests.Session()

def addSubscription(propertyId,header):

    if os.environ['env_variable'] == 'TEST':
        addSubscriptionApi=config['TestApi']['addsubscriptionapi'].replace('{propertyId}',str(propertyId))
    elif os.environ['env_variable'] == 'PRODUCTION':
        addSubscriptionApi=config['ProductionApi']['addsubscriptionapi'].replace('{propertyId}',str(propertyId))

    subscriptionList=['Booking Management','Revenue Management','Business Setup']

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
            print('Subscription add api status code',subscriptionStatusCode)
    
    return subscriptionStatusCode
