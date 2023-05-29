from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def login_to_site(driver, url, username_id, user_username, password_id, user_password, text):
    """ login to website using selenium """
    driver.get("https://public.emdat.be/login")


    time.sleep(1)
    username = driver.find_element_by_id("user")
    username.clear()
    username.send_keys(user_username)

    password = username = driver.find_element_by_id("password")
    password.clear()
    password.send_keys(user_password)

    driver.find_element_by_xpath('//button[contains(text(), "Log in")]').click()

    return driver
    
