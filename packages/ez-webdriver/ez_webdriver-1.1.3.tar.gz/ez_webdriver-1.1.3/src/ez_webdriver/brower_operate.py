import time

from ez_webdriver import chrome,firefox,clear_cache
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
"""
浏览器操作部分
"""


# 获取浏览器驱动
def start_chrome():
    driver = webdriver.Chrome(service=Service(chrome()))
    time.sleep(3)
    driver.close()

def start_firefox():
    driver = webdriver.Firefox(service=Service(firefox()))
    time.sleep(3)
    driver.close()
    driver.quit()

# start_firefox()
start_chrome()
clear_cache()























