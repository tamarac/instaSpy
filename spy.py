
import re
import time
import json
import pandas as pd
from datetime import datetime
import requests
from seleniumwire import webdriver 
from dotenv import dotenv_values
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.wait import WebDriverWait
import re

regex = r"https:\/\/i\.instagram\.com\/api\/v1\/friendships\/\d+\/"
regexExtract = r"\?count=\d+&"
config = dotenv_values(".env")
today = pd.to_datetime(datetime.now(), format='%Y-%m-%d %H:%M:%S')

regexClearText = r"\s.+"
accounts = config["SPY_ACCOUNTS"].split(',')

followers = []
followins = []

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
driver.get(config["DOMAIN"])

def login():
    time.sleep(3)
    username = driver.find_element_by_name('username')
    username.clear()
    username.send_keys(config['INSTA_ACCOUNT'])
    password = driver.find_element_by_name('password')
    password.send_keys(config['INSTA_PASSWORD'])
    login = driver.find_elements_by_css_selector("button.sqdOP.L3NKy.y3zKF")

    for e in login:
        if e.text == "Entrar":
            e.click()

    time.sleep(3)
    notNow = driver.find_elements_by_link_text("button.sqdOP.yWX7d.y3zKF")
    for e in notNow:
        e.click()

def clearText(text):
    return re.sub(regexClearText, "", text, 0, re.MULTILINE)

def getItemMenu(i):
    analyzedItems = driver.find_elements_by_css_selector("li.Y8-fY")
    analyzedItems[i].click()
    return analyzedItems

def closePopUp():
    close = driver.find_elements_by_css_selector(".WaOAr")
    close[1].click()

def transformData(data):
    result = {}
    for item in data:
        result[item['name']] = item['value']
def getDataFollowers(numfollowers):
    substitution = "?count=" + numfollowers + "&"
    for request in driver.requests:
        if request.response and re.search(regex, request.url):
            url = request.url
            newUrl = re.sub(regexExtract, substitution, url, 0, re.MULTILINE)
            headers = request.headers
            cookies =transformData(driver.get_cookies())
            r = requests.get(newUrl, data=[], headers=headers, cookies=cookies).json()
            print(len(r['users']))
            for user in r['users']:
                followers.append(user['username'])

def getDataFollowing(numfollowing):
    substitution = "?count=" + numfollowing + "&"
    for request in driver.requests:
        if request.response and re.search(regex, request.url):
            url = request.url
            newUrl = re.sub(regexExtract, substitution, url, 0, re.MULTILINE)
            headers = request.headers
            cookies =transformData(driver.get_cookies())
            r = requests.get(newUrl, data=[], headers=headers, cookies=cookies).json()
            print(len(r['users']))
            for user in r['users']:
                followers.append(user['username'])

def scrollDialog(number):
    fBody = WebDriverWait(driver, 2).until(lambda d: d.find_element_by_xpath("//div[@class='isgrP']"))
    time.sleep(2)
    scroll = 0
    while scroll < (int(number)/4):
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + (arguments[0].offsetHeight - 20);', fBody)
        time.sleep(3)
        driver.find_elements_by_xpath("//li.wo9IH")
        scroll += 1

def getListFollowers():
    listFollowers = driver.find_elements_by_css_selector("a.FPmhX.notranslate._0imsa")
    for item in listFollowers:
        followers.append(item.text)

def getListFollowins():
    listFollowins = driver.find_elements_by_css_selector("a.FPmhX.notranslate._0imsa")
    for item in listFollowins:
        followins.append(item.text)

def getInitialData():
    df = pd.read_json(path_or_buf='data/dados.json', orient='table')
 
    for account in accounts:
        driver.get(config["DOMAIN"] + account +"/")
        analyzedItems = getItemMenu(1)
        numPosts = clearText(analyzedItems[0].text)
        numfollowers = clearText(analyzedItems[1].text)
        numfollowins = clearText(analyzedItems[2].text)
        time.sleep(3)
        getDataFollowers(numfollowers)
        closePopUp()
        getItemMenu(2)
        time.sleep(3)
   
        scrollDialog(numfollowins)
        getListFollowins()
        closePopUp()

        jsonData = {
            "username": account,
            "posts": int(numPosts),
            "numberFollowers": int(numfollowers),
            "numberFollowins": int(numfollowins),
            "listFollowers": followers,
            "listFollowins": followins,
            "date": today
        }
       
        df = df.append(jsonData, ignore_index=True)
        df.to_json(path_or_buf='data/dados.json', orient="table")
        followers.clear()
        followins.clear()
    driver.close()