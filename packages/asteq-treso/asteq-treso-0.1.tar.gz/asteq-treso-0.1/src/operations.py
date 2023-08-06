# ----------------------------------------- IMPORTS -------------------------------------------------------
# Env variables
from dataclasses import dataclass,asdict
import os

import json

# Selenium 4 : Minimal imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Selenium locators
from selenium.webdriver.common.by import By

# Selenium Waits
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Selenium no logs
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# ----------------------------------------- VARIABLES -------------------------------------------------------

# Global variables
soge_path = "https://professionnels.societegenerale.fr/icd-web/syd-front/index-comptes.html#comptes"

# ----------------------------------------- CLASSES ---------------------------------------------------------

@dataclass
class Operation :
    date: str
    date_value: str
    nature: str
    debit: float
    credit: float
    solde_comptable:float

# ----------------------------------------- FUNCTIONS -------------------------------------------------------

def elementPresentCheck(driver, byWhat, path:str,callback=lambda x:x)->bool:
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((byWhat, path))
            )
        callback(element)
        return True
    except Exception as e:
        print(e)
        return False

def cookiePopUpCheck(driver)->bool:
    def callback(element):
        button = element.find_element(By.ID,"popin_tc_privacy_button_3")
        button.click()

    return elementPresentCheck(driver, By.ID, path="popin_tc_privacy",callback=callback)

def userInputCheck(driver,user_id:str=None):
    def callback(element):
        if user_id is not None :
            element.send_keys(user_id)

    return elementPresentCheck(driver,By.ID,path="user_id",callback=callback)

def operationArrayToJson(array:list[Operation])-> str:
    d = list(map(lambda x:asdict(x),array))
    return json.dumps(d,indent=4)
        
def betterParseInt(x:str)->float:
    string = x.replace(" ","").replace(",",".")
    if string == "" :
        return None
    return float(string)

# ----------------------------------------- MAIN -------------------------------------------------------


def fetchOperationsToJson():
    # Create driver instance
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
    driver.get(soge_path)

    # Check if Sogé asking for cookies and accept if then
    cookiePopUpCheck(driver)

    # Fill user_id field
    userInputCheck(driver, os.getenv('USER_ID'))

    print("Press Enter when you are ready to scrap")
    input()

    table = driver.find_element(By.ID,"idVirementList")
    releves = table.find_elements(By.CLASS_NAME,"button")

    releves_final = []
    for releve in releves:
        categories = releve.find_elements(By.TAG_NAME,"td")
        operation = Operation(
            date=categories[0].text,
            date_value=categories[1].text,
            nature=categories[2].text,
            debit=betterParseInt(categories[3].text),
            credit=betterParseInt(categories[4].text),
            solde_comptable=betterParseInt(categories[5].text),
        )
        releves_final.append(operation)
    releves_final.reverse()
    return operationArrayToJson(releves_final)