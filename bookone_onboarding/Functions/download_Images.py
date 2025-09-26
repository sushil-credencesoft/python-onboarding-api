from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

driver=webdriver.Chrome('chromedriver.exe')

keys='Srk villa malavli'
suburb='Winter Harvest Society'
city='Malavli'

driver.get('https://www.google.com/maps')
driver.find_element(by=By.XPATH,value='//*[@id="searchboxinput"]').send_keys(keys)
time.sleep(5)

src=driver.page_source
soup=BeautifulSoup(src,'lxml')

containers=soup.find_all('div',class_='sW9vGe')
for c in containers:
    if ',' in c.text and city in c.text and suburb in c.text:
        target=c.text.replace('Ad','')
        driver.find_element(by=By.XPATH,value='//*[@id="searchboxinput"]').send_keys(target)
        time.sleep(2)
        driver.find_element(by=By.XPATH,value='//*[@id="searchbox-searchbutton"]').click()
        time.sleep(5)
        driver.find_element(by=By.XPATH,value='//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/button').click()
        time.sleep(5)

        allImages=driver.find_elements(by=By.CLASS_NAME,value='U39Pmb')
        for a in allImages:
            driver.execute_script("arguments[0].click();", a)
            src2=driver.page_source
            soup2=BeautifulSoup(src2,'lxml')
            imageList=soup2.find_all('div',class_='U39Pmb')
            for i in imageList:
                print(i['style'])
            print('---------------------')
            time.sleep(3)
        
        

        
        
