import selenium

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# function for initalizing telegram
def init_telegram():
    options = Options()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    telegram = driver.get('https://web.telegram.org/a/')
    driver.maximize_window()
    return driver

# function for sending a message
def send_msg(driver, url, message):
    link = driver.find_element(By.XPATH, f"//a[@href='{url}']")
    link.click()
    time.sleep(1)
    while True:
        try:
            textbox = driver.find_element(By.ID, 'editable-message-text')
            textbox.send_keys(message)
            textbox.send_keys(Keys.RETURN)
            break
        except:
            print('loading...')

# function for reading unread message
def read_new_msg(driver, url):
    link = driver.find_element(By.XPATH, f"//a[@href='{url}']")
    try:
        new_msg = link.find_element(By.CLASS_NAME, "ChatBadge.unread")
        new_msg = new_msg.text
        count = int(new_msg)
        link.click()
        msgs = driver.find_elements(By.CLASS_NAME, 'text-content.clearfix.with-meta')
        for i in range(len(msgs) - count, len(msgs)):
            print(msgs[i].text)
    except:
        print('No new messages')

