# import requests
# from datetime import datetime as dt
# from datetime import timedelta
# import time
# from urllib3.util.retry import Retry
# from requests.adapters import HTTPAdapter




# session = requests.Session()
# retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
# adapter = HTTPAdapter(max_retries=retries)
# session.mount('http://', adapter)
# session.mount('https://', adapter)

# def addOrupdatePlan(property_id):
#     try:
                
#                 print(f"Property ID for : {property_id}")
#                 property_rooms_url = f'https://api.thehotelmate.co/api/property/{property_id}/rooms'
#                 property_rooms_response = requests.get(property_rooms_url)
                

#                 if property_rooms_response.status_code == 200:
                    
#                     property_rooms_data = property_rooms_response.json()

                    

#                     for room in property_rooms_data:
                        
#                         print("Room ID:", room.get('id'))
#                         print("Room Only Price:", room.get('roomOnlyPrice'))
#                         print("Number of Rooms:", room.get('noOfRooms'))
#                         room_id = room.get('id')

#                         room_plan_url = f'https://api.thehotelmate.co/api/room/property/{property_id}/room/{room_id}/roomPlan'
#                         room_plan_response = requests.get(room_plan_url)

 


#                         if room_plan_response.status_code == 200:
#                             room_plan_data = room_plan_response.json()

#                             for avail_plan in room_plan_data:
                                
#                                     # avail_plan["channelManagerUpdateType"] = "ROOM_RATE_PLAN"
#                                     avail_plan["propertyId"] = property_id
#                                     avail_plan["roomTypeId"] = room_id

#                                     current_date = dt.today()

#                                     avail_plan["effectiveDate"] = current_date.strftime("%Y-%m-%d")
#                                     avail_plan["expiryDate"] = "2027-12-31"

#                                     avail_plan["isApplicableToOta"] = True
#                                     print(avail_plan["name"])

#                                     plan_details_url = f"https://api.thehotelmate.co/api/room/property/{property_id}/room/{room_id}/roomPlan"
#                                     plan_response = session.post(plan_details_url,json=avail_plan)
#                                     if plan_response.status_code in [200,201]:
#                                         print("updated plan details successful")

#                                         # Calculate the date one day later
#                                         today = current_date + timedelta(days=0)

#                                         one_month_later = today + timedelta(days=10)  


#                                         formatted_current_date = today.strftime("%Y-%m-%d")
#                                         formatted_one_month_later = one_month_later.strftime("%Y-%m-%d")
                                    
#                                         avail_plan["effectiveDate"] = formatted_current_date
#                                         avail_plan["expiryDate"] = formatted_one_month_later
#                                         print("effectiveDate:", formatted_current_date)
#                                         print("expiryDate:", formatted_one_month_later)

#                                         avail_post = 'https://api.thehotelmate.co/api/availability/addOrUpdatePlan'
#                                         # Send the POST request for availability plan
#                                         response_avail_post = session.post(avail_post, json=avail_plan)

#                                         # Check if the request was successful (status code 200)
#                                         if response_avail_post.status_code == 200:
#                                             post_avail = response_avail_post.json()
#                                             print("POST Availability Plan Response:", post_avail)
#                                             time.sleep(5)
#                                         else:
#                                             print("Availability plan API request failed. Status code:", response_avail_post.status_code)
#                                             print("Response", response_avail_post.content)
#                                             time.sleep(10)
#                         else:
#                             print(f"Failed to fetch room plan. Status code: {room_plan_response.status_code}")
#                 else:
#                     print(f"Failed to fetch property rooms. Status code: {property_rooms_response.status_code}")
#     except Exception as e:
#         print("Exception arised, code:" ,e)


