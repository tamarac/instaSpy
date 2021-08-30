
import re
import time
import json
import pandas as pd
from datetime import datetime
from selenium import webdriver
from dotenv import dotenv_values
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.wait import WebDriverWait

config = dotenv_values(".env")
today = datetime.today()
regexClearText = r"\s.+"
vitimas = config["SPY_ACCOUNTS"].split(',')

seguidores = []
seguindo = []

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
driver.get(config["DOMAIN"])

def login():
    time.sleep(3)
    username = driver.find_element_by_name('username')
    username.clear()
    username.send_keys(config['INSTA_ACCOUNT'])
    password = driver.find_element_by_name('password')
    password.send_keys(config['INSTA_PASSWORD'])
    entrar = driver.find_elements_by_css_selector("button.sqdOP.L3NKy.y3zKF")

    for e in entrar:
        if e.text == "Entrar":
            e.click()

    time.sleep(3)
    agrNao = driver.find_elements_by_link_text("button.sqdOP.yWX7d.y3zKF")
    for e in agrNao:
        e.click()

def clearText(text):
    return re.sub(regexClearText, "", text, 0, re.MULTILINE)

def getItemMenu(i):
    itemsAnalisados = driver.find_elements_by_css_selector("li.Y8-fY")
    itemsAnalisados[i].click()
    return itemsAnalisados

def closePopUp():
    close = driver.find_elements_by_css_selector(".QBdPU")
    close[1].click()

def getListFollowers():
    listaSeguidores = driver.find_elements_by_css_selector("a.FPmhX.notranslate._0imsa")
    for item in listaSeguidores:
        seguidores.append(item.text)

def scrollDialog(number):
    fBody = WebDriverWait(driver, 2).until(lambda d: d.find_element_by_xpath("//div[@class='isgrP']"))
    time.sleep(2)
    scroll = 0
    while scroll < (int(number)/4):
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + (arguments[0].offsetHeight - 20);', fBody)
        time.sleep(1)
        driver.find_elements_by_xpath("//li.wo9IH")
        scroll += 1
       

def getListFollowers():
    listaSeguidores = driver.find_elements_by_css_selector("a.FPmhX.notranslate._0imsa")
    for item in listaSeguidores:
        seguidores.append(item.text)

def getListFollowins():
    listaSeguindo = driver.find_elements_by_css_selector("a.FPmhX.notranslate._0imsa")
    for item in listaSeguindo:
        seguindo.append(item.text)

def getInitialData():
    df = pd.read_json(path_or_buf='data/dados.json', orient='table')
    print(df)
    for vitima in vitimas:
        driver.get(config["DOMAIN"] + vitima +"/")
        itemsAnalisados = getItemMenu(1)
        numPosts = clearText(itemsAnalisados[0].text)
        numSeguidores = clearText(itemsAnalisados[1].text)
        numSeguindo = clearText(itemsAnalisados[2].text)
        time.sleep(3)

        scrollDialog(numSeguidores)
        getListFollowers()
        closePopUp()
        getItemMenu(2)
        time.sleep(3)
   
        scrollDialog(numSeguindo)
        getListFollowins()
        closePopUp() 

        jsonData = {
            "username": vitima,
            "posts": numPosts,
            "qntSeguidores": numSeguidores,
            "qntSeguindo": numSeguindo,
            "listaSeguidores": seguidores,
            "listaSeguindo": seguindo,
            "date": str(today)
        }
       
        df = df.append(jsonData, ignore_index=True)
        result = df.to_json(path_or_buf='data/dados.json', orient="table")

        parsed = json.loads(result)
        json.dumps(parsed, indent=4) 
        seguidores.clear()
        seguindo.clear()