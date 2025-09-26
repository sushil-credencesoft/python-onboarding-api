# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# import time
# from selenium import webdriver

# # give the page links below 
# pageLinks=[]

# # give the selenium path below 
# driver=webdriver.Chrome('')


# for x in pageLinks:
#     driver.get(x['url'])

#     reached_page_end = False
#     last_height = driver.execute_script("return document.body.scrollHeight")

#     while not reached_page_end:
#         driver.find_element(by=By.XPATH, value='//body').send_keys(Keys.END)   
#         time.sleep(2)
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         if last_height == new_height:
#             reached_page_end = True
#         else:
#             last_height = new_height