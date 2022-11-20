from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
import os

def openFirefox(HeadLess, Url):
    options = webdriver.FirefoxOptions()
    options.headless = HeadLess     #Headless mode!!
    driver = webdriver.Firefox(options=options)
    driver.get(Url)
    return driver

def closeFirefox(driver):
    driver.close()

def openChrome(Url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    #driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(Url)
    return driver

def closeChrome(driver):
    driver.close()

def findByCSS(Where, Delay, driver):
    wait = WebDriverWait(driver, 100)
    elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, Where)))
    sleep(Delay)
    elem = driver.find_element(By.CSS_SELECTOR, Where)
    return elem.text

def findsByID(Where, Delay, driver):
    wait = WebDriverWait(driver, Delay)
    try:
        elem = wait.until(EC.element_to_be_clickable((By.ID, Where)))
        #sleep(Delay)
        elem = driver.find_element(By.ID, Where)
        return elem.text
    except:
        return "End"

def findsByCLASS(Where, Delay, driver):
    wait = WebDriverWait(driver, Delay)
    try:
        elem = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, Where)))
        #sleep(Delay)
        elem = driver.find_element(By.CLASS_NAME, Where)
        return elem.text
    except:
        return "End"

def findsByXpath(Where, Delay, driver):
    wait = WebDriverWait(driver, Delay)
    try:
        elem = wait.until(EC.element_to_be_clickable((By.XPATH, Where)))
        #sleep(Delay)
        elem = driver.find_element(By.XPATH, Where)
        return elem.text
    except:
        return "End"

def findByID(Where, Delay, driver):
    wait = WebDriverWait(driver, 100)
    elem = wait.until(EC.element_to_be_clickable((By.ID, Where)))
    sleep(Delay)
    elem = driver.find_element(By.ID, Where)
    return elem.text

def insertTextByID(Where,Delay, Text, driver):
    wait = WebDriverWait(driver, 100)
    elem = wait.until(EC.element_to_be_clickable((By.ID, Where)))
    sleep(Delay)
    elem = driver.find_element(By.ID, Where)
    elem.clear()
    elem.send_keys(Text)

def insertTextByCSS(Where, Delay, Text, driver):
    wait = WebDriverWait(driver, 100)
    elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, Where)))
    sleep(Delay)
    elem = driver.find_element(By.CSS_SELECTOR, Where)
    elem.clear()
    elem.send_keys(Text)  

def insertDateByCSS(Where, Delay, WhereDate, Text, driver):
    wait = WebDriverWait(driver, 100)
    elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, Where)))
    sleep(Delay)
    elem = driver.find_element(By.CSS_SELECTOR, WhereDate)
    action = ActionChains(driver)
    action.click(on_element = elem)
    action.perform()  
    elem = driver.find_element(By.CSS_SELECTOR, Where)
    action = ActionChains(driver)
    action.key_down(Keys.CONTROL).send_keys('A').key_up(Keys.CONTROL).perform()
    elem.send_keys(Text)  

def clickOnID(Where, Delay, driver):
    wait = WebDriverWait(driver, 100)
    elem = wait.until(EC.element_to_be_clickable((By.ID, Where)))
    sleep(Delay)
    elem = driver.find_element(By.ID, Where)
    action = ActionChains(driver)
    action.click(on_element = elem)  # click the item  
    action.perform()        # perform the operation

def clickOnCSS(Where, Delay, driver):
    wait = WebDriverWait(driver, 100)
    elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, Where)))
    sleep(Delay)
    elem = driver.find_element(By.CSS_SELECTOR, Where)
    action = ActionChains(driver)
    action.click(on_element = elem)  # click the item  
    action.perform()

def clickOnXpath(Where, Delay, driver):
    wait = WebDriverWait(driver, 100)
    elem = wait.until(EC.element_to_be_clickable((By.XPATH, Where)))
    sleep(Delay)
    elem = driver.find_element(By.XPATH, Where)
    action = ActionChains(driver)
    action.click(on_element=elem)  # click the item
    action.perform()