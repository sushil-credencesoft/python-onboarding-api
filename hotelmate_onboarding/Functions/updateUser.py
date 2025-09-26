import requests
import os
from hotelmate_onboarding.helper import read_config

config = read_config()

s=requests.Session()

def updateUser(userId,businessType,businessEmail,password,businessName,mobileNumber,city,suburb,streetName,country,state,postcode,adminFirstName,adminLastName):
    
    updateUserdata =  {
   "plan":"Business Premium",
   "organisationId":1,
   "businessType":businessType,
   "businessTypeGroup":"TRAVEL & TOURISM",
   "email":businessEmail,
   "password":password,
   "confirmPassword":password,
   "id":userId,
   "businessName":businessName,
   "firstName":adminFirstName,
   "lastName":adminLastName,
   "mobileNumber":"",
   "address":{
      "city":city,
      "suburb":suburb,
      "streetNumber":"",
      "streetName":streetName,
      "state":state,
      "country":country,
      "postcode":postcode
   },
   "dashboardUrl":"https://testapp.bookonelocal.co.nz",
   "username":"hotelworld03@gmail.com",
   "userStatus":"NEW"
}


    if os.environ['env_variable'] == 'TEST':
        updateUserApi=config['TestApi']['updateuserapi']
    elif os.environ['env_variable'] == 'PRODUCTION':
        updateUserApi=config['ProductionApi']['updateuserapi']

    updateUser = requests.post(updateUserApi, json=updateUserdata)
    updateUserStatusCode = updateUser.status_code
    print(updateUserStatusCode)
    if updateUserStatusCode == 200:
        print('User data update api status code',updateUserStatusCode)
    
    return updateUserStatusCode

    