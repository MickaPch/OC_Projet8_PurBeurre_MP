"""Selenium Test"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome()
driver.get('/')
assert 'Pur Beurre' in driver.title


driver.close()