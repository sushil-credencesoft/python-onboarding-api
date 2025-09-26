import requests

propertyId = 1166
userId = "1423"
apiToken = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJzYWJlcmFyZXNpZGVuY3lAZ21haWwuY29tIiwic2NvcGVzIjoiUk9MRV9QUk9QX0FETUlOIiwiaWF0IjoxNjg4OTE4MDQ1LCJleHAiOjE2ODkzNTAwNDV9.nDuew_xW4HbpDI_csJmHCfLNIjUtXKpe2SPnv5jUX-E"

header = {
    'USER_ID': userId,
    'Authorization': apiToken,
    'APP_ID': 'BOOKONE_WEB_APP'

}
deleteUserApi = f'https://api.thehotelmate.co/hotelmate/api/property/user/delete/{propertyId}'
deletePropertyApi = f'https://api.thehotelmate.co/hotelmate/api/property/delete/{propertyId}'

request = requests.Session()
deleteUserApiCall = request.post(deleteUserApi, headers=header)
if deleteUserApiCall.status_code == 200:
    print('user deleted successfully', deleteUserApiCall.status_code)
    deletePropertyApiCall = request.post(deletePropertyApi, headers=header)
    print('Property deleted successfully', deletePropertyApiCall.status_code)
else:
    print('User is not deleted.', deleteUserApiCall.status_code)
