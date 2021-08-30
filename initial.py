
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from spy import getInitialData, login

#driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

login()

getInitialData()
#driver.close()