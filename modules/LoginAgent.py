from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from time import sleep
import os

class LoginAgent():
    def __init__(self,phone):
        self.phoneNumber = phone
    
    def AutomatedLogin(self):
        driver = self.LoginWithProfile()

        if driver.find_elements(By.CLASS_NAME,"c1p6lbu0") != None:
            elements = driver.find_elements(By.CLASS_NAME,"c1p6lbu0")
            buttons = ["Elfogadom","Jelentkezz be"]
            for button in buttons:
                for el in elements:
                    if el.text == button:
                        el.click()
                        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'c1p6lbu0')))
                        break
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@aria-labelledby="MODAL_LOGIN"]')))
            buttons = ["Bejelentkezés telefonszámmal","Következő"]
            for button in buttons:
                elements = driver.find_elements(By.XPATH, '//*[@aria-labelledby="MODAL_LOGIN"]')
                for el in elements:
                    try:
                        if el.find_element(By.ID, "phone_number").is_displayed:
                            el.find_element(By.ID, "phone_number").send_keys(self.phoneNumber)
                    except:
                        pass
                    results = el.find_elements(By.CLASS_NAME,"c1p6lbu0")
                    for result in results:
                        if result.text == button:
                            result.click()
                            break
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@aria-labelledby="MODAL_LOGIN"]')))
                sleep(10)
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'c1p6lbu0')))
        return driver
    
    def LoginWithProfile(self):
        try:
            chrome_options = Options()
            chrome_options.add_argument(f"--start-maximized")
            chrome_options.add_argument(f"user-data-dir=os.getcwd()}/profile/")
            driver = webdriver.Chrome(options=chrome_options)
            driver.get("https://tinder.com/hu")
            sleep(3)
            return driver
        except Exception as e:
            profile = FirefoxProfile(f"{os.getcwd()}/profile/")
            options = Options()
            options.add_argument("--start-maximized")
            driver = webdriver.Firefox(firefox_profile=profile, options=options)
            driver.get("https://tinder.com/hu")
            sleep(3)
            return driver