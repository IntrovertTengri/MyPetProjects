import webbrowser
import selenium

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def init_youtube():
    options = Options()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    telegram = driver.get('https://youtube.com')
    driver.maximize_window()
    return driver

def search_video(name, driver):
    wait = WebDriverWait(driver, 3)
    presence = EC.presence_of_element_located
    visible = EC.visibility_of_element_located
    driver.get('https://www.youtube.com/results?search_query={}'.format(name))
    wait.until(visible((By.ID, "video-title")))
    driver.find_element(By.ID, "video-title").click()
    return driver