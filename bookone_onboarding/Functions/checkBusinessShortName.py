import requests
import os
from bookone_onboarding import helper

config=helper.read_config()

s=requests.Session()

def checkBusinessShortName(header,businessShortName):
    
    if os.environ['env_variable'] == 'TEST':
        checkBusinessShortNameApi=config['TestApi']['checkbusinessshortnameapi']
    elif os.environ['env_variable'] == 'PRODUCTION':
        checkBusinessShortNameApi=config['ProductionApi']['checkbusinessshortnameapi']

    b={
        'shortName':businessShortName
    }

    checkBusinessShortNamePresent=s.get(checkBusinessShortNameApi,params=b,headers=header)
    
    returnData=str(checkBusinessShortNamePresent.content).replace('b','').replace("'",'')
    print('return data',returnData)

    return returnData

      


    
    

