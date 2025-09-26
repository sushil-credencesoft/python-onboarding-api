import requests

s=requests.Session()

t='eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0Lm9uYm9hcmRpbmc1NEBnbWFpbC5jb20iLCJzY29wZXMiOiJST0xFX1BST1BfQURNSU4iLCJpYXQiOjE2Nzk3NDczMDcsImV4cCI6MTY4MDE3OTMwN30.tKPJNSRDuK6Pa--n76_9YduuCKOvWupjG-KnX6-Erxg'
token=f'Bearer {t}'

header = {
            'Authorization': token,
            'APP_ID': 'BOOKONE_WEB_APP'
        }

findUserApiCall=s.get(f'https://testapi.bookonelocal.co.nz/api-bookone/api/property/findByUserId/1253',headers=header)
print(findUserApiCall.status_code)
print(findUserApiCall.content)