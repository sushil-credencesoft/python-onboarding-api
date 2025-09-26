# TBD :
'''

The main purpose of this script is to select the config file either for test or prod as per the requirement.

'''

import configparser

config_file = configparser.ConfigParser()

config_file.add_section('TestApi')

config_file.set('TestApi', 'signupapi',
                'https://testapi.bookonelocal.co.nz/api-bookone/api/user/signup')
config_file.set('TestApi', 'loginapi',
                'https://testapi.bookonelocal.co.nz/api-bookone/api/user/login')
config_file.set('TestApi', 'findbyuser',
                'https://testapi.bookonelocal.co.nz/api-bookone/api/property/findByUserId/{userID}')
config_file.set('TestApi', 'updateproperty',
                'https://testapi.bookonelocal.co.nz/api-bookone/api/property/user/update/property')
config_file.set('TestApi', 'updateuserapi',
                'https://testapi.bookonelocal.co.nz/api-bookone/api/user/updateUser')
config_file.set('TestApi', 'addpropertyapi',
                'https://testapi.bookonelocal.co.nz/api-bookone/api/property/user/add/property')
config_file.set('TestApi', 'addsubscriptionapi',
                'https://testapi.bookonelocal.co.nz/api-bookone/api/property/{propertyId}/addSubscription')
config_file.set('TestApi', 'addroomapi',
                'https://testapi.bookonelocal.co.nz/api-bookone/api/property/{propertyId}/user/add/room')
config_file.set('TestApi', 'getroomdetailsapi',
                'https://testapi.bookonelocal.co.nz/api-bookone/api/property/{propertyId}/rooms')
config_file.set('TestApi', 'addroomplanapi',
                'https://testapi.bookonelocal.co.nz/api-bookone/api/room/property/{propertyId}/room/{individualRoomId}/roomPlan')
config_file.set('TestApi', 'yearlygenerateratesapi',
                'https://testapi.bookonelocal.co.nz/api-bookone/api/property/addYearlyRates')
config_file.set('TestApi', 'pointofsaleapi',
                'https://testapi.bookonelocal.co.nz/api-bookone/api/property/{propertyId}/pointOfSale')
config_file.set('TestApi', 'businessserviceapi',
                'https://testapi.bookonelocal.co.nz/api-bookone/api/businessService')
config_file.set('TestApi', 'addavailabilitybydate',
                'https://testapi.bookonelocal.co.nz/api-bookone/api/availability/addAvailabilityByRoomAndDateRange')
config_file.set('TestApi', 'addorupdateplanapi',
                'https://testapi.bookonelocal.co.nz/api-bookone/api/availability/addOrUpdatePlan')
config_file.set('TestApi', 'checkbusinessshortnameapi',
                'https://testapi.bookonelocal.co.nz/api-bookone/api/property/findByShortName')
config_file.set('TestApi', 'deletepropertyapi',
                'https://testapi.bookonelocal.co.nz/api/property/delete/{propertyId}')
config_file.set('TestApi', 'deleteuserapi',
                'https://testapi.bookonelocal.co.nz/api-bookone/api/property/user/delete/{propertyId}')
config_file.set('TestApi', 'addroomdetailsapi',
                'https://testapi.bookonelocal.co.nz/api-bookone/api/room/property/{propertyId}/room/{extractedRoomId}/add/roomDetails')
config_file.set('TestApi', 'addgstapi',
                'https://testapi.bookonelocal.co.nz/api-bookone/api/property/user/update/property')
config_file.set('TestApi', 'opendaysserviceapi',
                'https://testapi.bookonelocal.co.nz/api-bookone/api/businessService/{serviceID}/openDays')
config_file.set('TestApi', 'taxdetailsapi',
                'https://testapi.bookonelocal.co.nz/api-bookone/api/businessService/{serviceID}/taxDetails')
config_file.set('TestApi', 'businessprofileupdateapi',
                'https://testapi.bookonelocal.co.nz/api-bookone/api/property/user/update/property')
config_file.set('TestApi', 'modeofpaymentapi',
                'https://testapi.bookonelocal.co.nz/api-bookone/api/propertyPayment/create')
config_file.set('TestApi', 'otaApi',
                'https://testapi.bookonelocal.co.nz/api-bookone/api/room/addOtaPlan/room/{roomId}')

config_file.add_section('ProductionApi')

config_file.set('ProductionApi', 'signupapi',
                'https://api.bookonelocal.in/api-bookone/api/user/signup')
config_file.set('ProductionApi', 'loginapi',
                'https://api.bookonelocal.in/api-bookone/api/user/login')
config_file.set('ProductionApi', 'findbyuser',
                'https://api.bookonelocal.in/api-bookone/api/property/findByUserId/{userID}')
config_file.set('ProductionApi', 'updateproperty',
                'https://api.bookonelocal.in/api-bookone/api/property/user/update/property')
config_file.set('ProductionApi', 'updateuserapi',
                'https://api.bookonelocal.in/api-bookone/api/user/updateUser')
config_file.set('ProductionApi', 'addpropertyapi',
                'https://api.bookonelocal.in/api-bookone/api/property/user/add/property')
config_file.set('ProductionApi', 'addsubscriptionapi',
                'https://api.bookonelocal.in/api-bookone/api/property/{propertyId}/addSubscription')
config_file.set('ProductionApi', 'addroomapi',
                'https://api.bookonelocal.in/api-bookone/api/property/{propertyId}/user/add/room')
config_file.set('ProductionApi', 'getroomdetailsapi',
                'https://api.bookonelocal.in/api-bookone/api/property/{propertyId}/rooms')
config_file.set('ProductionApi', 'addroomplanapi',
                'https://api.bookonelocal.in/api-bookone/api/room/property/{propertyId}/room/{individualRoomId}/roomPlan')
config_file.set('ProductionApi', 'yearlygenerateratesapi',
                'https://api.bookonelocal.in/api-bookone/api/property/addYearlyRates')
config_file.set('ProductionApi', 'pointofsaleapi',
                'https://api.bookonelocal.in/api-bookone/api/property/{propertyId}/pointOfSale')
config_file.set('ProductionApi', 'businessserviceapi',
                'https://api.bookonelocal.in/api-bookone/api/businessService')
config_file.set('ProductionApi', 'addavailabilitybydate',
                'https://api.bookonelocal.in/api-bookone/api/availability/addAvailabilityByRoomAndDateRange')
config_file.set('ProductionApi', 'addorupdateplanapi',
                'https://api.bookonelocal.in/api-bookone/api/availability/addOrUpdatePlan')
config_file.set('ProductionApi', 'checkbusinessshortnameapi',
                'https://api.bookonelocal.in/api-bookone/api/property/findByShortName')
config_file.set('ProductionApi', 'deletepropertyapi',
                'https://testapi.bookonelocal.co.nz/api/property/delete/{propertyId}')
config_file.set('ProductionApi', 'deleteuserapi',
                'https://api.bookonelocal.in/api-bookone/api/property/user/delete/{propertyId}')
config_file.set('ProductionApi', 'addroomdetailsapi',
                'https://api.bookonelocal.in/api-bookone/api/room/property/{propertyId}/room/{extractedRoomId}/add/roomDetails')
config_file.set('ProductionApi', 'addgstapi',
                'https://api.bookonelocal.in/api-bookone/api/property/user/update/property')
config_file.set('ProductionApi', 'opendaysserviceapi',
                'https://api.bookonelocal.in/api-bookone/api/businessService/{serviceID}/openDays')
config_file.set('ProductionApi', 'taxdetailsapi',
                'https://api.bookonelocal.in/api-bookone/api/businessService/{serviceID}/taxDetails')
config_file.set('ProductionApi', 'businessprofileupdateapi',
                'https://api.bookonelocal.in/api-bookone/api/property/user/update/property')
config_file.set('ProductionApi', 'modeofpaymentapi',
                'https://api.bookonelocal.in/api-bookone/api/propertyPayment/create')
config_file.set('ProductionApi', 'otaApi',
                'https://api.bookonelocal.in/api-bookone/api/room/addOtaPlan/room/{roomId}')

with open(r"configurations.ini", 'w') as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()
    configfileObj.close()
