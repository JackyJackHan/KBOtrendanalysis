import itertools
import os
from bs4 import BeautifulSoup
from html_table_parser import parser_functions

import pandas as pd
import sys
import parser
import requests
import datetime

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from openpyxl import Workbook

chrome_driver = 'C:/chromedriver'

from selenium import webdriver
import sys
from pathlib import Path

from getch import pause
import time

driver = webdriver.Chrome(chrome_driver)

url = "https://sports.news.naver.com/kbaseball/news/index?page=1&date=20210101&isphoto=N&type=latest"

driver.get(url)

start_date = pd.to_datetime("2021-10-31")
end_date = pd.to_datetime("2021-12-31")

dates = pd.date_range(start_date, end_date, freq='D')

initial = [("2021-01-01", "Title", "Body")]
df = pd.DataFrame(initial, columns=['Date', 'Title', 'Body'])

for i in range(0, len(dates) + 1):
    url2 = url[0:56] + str(1) + url[57:63] + dates.strftime('%Y%m%d')[i] + url[71:]
    driver.get(url2)
    time.sleep(0.5)

    try:
        next = driver.find_element_by_xpath('// *[ @ id = "_pageList"] / a[10]')
    except:
        next = None

    if next != None:
        pagelength = driver.find_elements_by_xpath('//*[@id="_pageList"]/a')

        for j in range(1, len(pagelength) + 1):

            url3 = url[0:56] + str(j) + url[57:63] + dates.strftime('%Y%m%d')[i] + url[71:]
            driver.get(url3)
            time.sleep(0.5)

            newslinks = driver.find_elements_by_xpath('//*[@id="_newsList"]/ul/li/div/a')
            newsurl = []

            for n in newslinks:
                href = n.get_attribute('href')
                newsurl.append(href)

            for k in newsurl:
                driver.get(k)
                title = driver.find_element_by_xpath(
                    '// *[ @ id = "content"] / div / div[1] / div / div[1] / h4').text
                body = driver.find_element_by_xpath('//*[@id="newsEndContents"]').text
                df = df.append({'Date': dates.strftime('%Y%m%d')[i], 'Title': title, 'Body': body}, ignore_index=True)

        driver.get(url3)
        time.sleep(0.5)
        next = driver.find_element_by_xpath('// *[ @ id = "_pageList"] / a[10]')
        next.click()
        time.sleep(0.5)
        pagelength = driver.find_elements_by_xpath('//*[@id="_pageList"]/a')

        for j in range(10, 10 + len(pagelength) + 1):

            driver.get(url[0:56] + str(j) + url[57:63] + dates.strftime('%Y%m%d')[i] + url[71:])
            time.sleep(1)
            newslinks = driver.find_elements_by_css_selector('#_newsList > ul > li > div > a')
            newsurl = []

            for n in newslinks:
                href = n.get_attribute('href')
                newsurl.append(href)

            for k in newsurl:
                driver.get(k)
                title = driver.find_element_by_xpath(
                    '// *[ @ id = "content"] / div / div[1] / div / div[1] / h4').text
                body = driver.find_element_by_xpath('//*[@id="newsEndContents"]').text
                df = df.append({'Date': dates.strftime('%Y%m%d')[i], 'Title': title, 'Body': body}, ignore_index=True)

    if next == None:

        pagelength = driver.find_elements_by_xpath('//*[@id="_pageList"]/a')

        for j in range(1, len(pagelength) + 1):

            driver.get(url[0:56] + str(j) + url[57:63] + dates.strftime('%Y%m%d')[i] + url[71:])

            time.sleep(1)

            newslinks = driver.find_elements_by_css_selector('#_newsList > ul > li > div > a')
            newsurl = []

            for n in newslinks:
                href = n.get_attribute('href')
                newsurl.append(href)

            for k in newsurl:
                driver.get(k)
                title = driver.find_element_by_xpath(
                    '// *[ @ id = "content"] / div / div[1] / div / div[1] / h4').text
                body = driver.find_element_by_xpath('//*[@id="newsEndContents"]').text
                df = df.append({'Date': dates.strftime('%Y%m%d')[i], 'Title': title, 'Body': body}, ignore_index=True)

##df.to_excel("News7.xlsx", index_label=False)

driver.get("http://www.statiz.co.kr/stat_at.php?mid=stat_at&re=0&ys=2020&ye=2021&se=0&te=&tm=&ty=2015&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR_ALL_ADJ&o2=TPA&de=1&lr=0&tr=&cv=&ml=1&pa=0&si=&cn=&sn=100")

i=1

initial= [("팀","이름")]
df2=pd.DataFrame(initial,columns=['Team',"Name"])

for i in range(1,11):

    playernamexpath='//*[@id="cphContents_cphContents_cphContents_udpRecord"]/div/table/tbody/tr['+str(i)+']/td/ul/li'
    teamnamexpath='//*[@id="cphContents_cphContents_cphContents_udpRecord"]/div/table/tbody/tr['+str(i)+']/th'
    teamname=driver.find_element(By.XPATH,teamnamexpath).text
    playerlist = driver.find_elements(By.XPATH,playernamexpath)

    for j in range(0, len(playerlist)):
        df2=df2.append({'Team':teamname,'Name':playerlist[j].text},ignore_index=True)

Players=pd.merge(df,df2,left_on=("Team","Name"),right_on=("Team","Name"),how='outer')

Players.to_csv("KBOPlayers.csv",encoding="EUC-KR")