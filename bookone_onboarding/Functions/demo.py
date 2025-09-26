# import requests

# api=f'https://testapi.bookonelocal.co.nz/api-bookone/api/file/fileUploadCloudBookingApp'

# user_id=504
# propertyId=518
# auth_token='Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJib29rb25lcHJvcGVydHkwMUBnbWFpbC5jb20iLCJzY29wZXMiOiJST0xFX1BST1BfQURNSU4iLCJpYXQiOjE2ODU5NjA1NTYsImV4cCI6MTY4NjM5MjU1Nn0.M2r6TrSdLclxnGBYrixR5WEUQVZvX2udaC2JqAR0WXs'
# file='businessImages\_NiloyGuestHouse\picture2.jpg'
# f=open(file,'rb')
# payload={
#     "file":f
# }

# header = {
#             'USER_ID': str(user_id),
#             'Authorization': auth_token,
#             'APP_ID': 'BOOKONE_WEB_APP'
#         }

# request=requests.Session()
# fileUploadApi=request.post(api,files=payload,headers=header)
# print(fileUploadApi.status_code)
# print(fileUploadApi.content)
#--------------------------------------------------------------------
import requests

header = {
            'USER_ID': str(1348),
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJob3RlbHByaXlhMDRAZ21haWwuY29tIiwic2NvcGVzIjoiUk9MRV9QUk9QX0FETUlOIiwiaWF0IjoxNjg2MTE1NDE3LCJleHAiOjE2ODY1NDc0MTd9.OwKJ1N5kY9IH9e_62_lc6eAmaMFLAE3GACoRwf_U3hE',
            'APP_ID': 'BOOKONE_WEB_APP',
            'Content-Type':'application/json',
            'Accept':'application/json'
        }
propertyId=2507

delete_user_api=f'https://testapi.bookonelocal.co.nz/api-bookone/api/property/user/delete/{propertyId}'
delete_property_api=f'https://testapi.bookonelocal.co.nz/api/property/delete/{propertyId}'

request=requests.Session()


delete_user=request.delete(delete_user_api,headers=header)
print('user deleted successfully', delete_user.status_code)

if delete_user.status_code==200:
    delete_property=request.delete(delete_property_api,headers=header)
    print('property deleted successfully', delete_property.status_code)
else:
    print('User is not deleted ,because of this property can not be deleted!')