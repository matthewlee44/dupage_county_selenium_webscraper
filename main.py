from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import pandas as pd


DRIVER_PATH = "/Users/admin/Downloads/chromedriver"

driver = webdriver.Chrome(executable_path = DRIVER_PATH)

def get_pin_page_source(driver, pin):

    url = "https://www.dupagecounty.gov/propertyinfo/propertylookup.aspx"

    driver.get(url)

    driver.find_element(By.ID, "ctl00_pageContent_ctl00_txtParcel").send_keys(pin + Keys.ENTER)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "tabid04")))

    return driver.page_source


def save_parcel_page(driver, pin):
        
    # Create string for pin to be used in URL
    url_pin = pin.replace("-", "")

    # Filename for parcel page HTML
    filename = f"./dupage_county_tax_files/{pin}.html"

    # If html file for PIN already exists in directory, skip it
    if not os.path.exists(filename):
    
        try:
            # Try getting to Parcel Page HTML with selenium

            html = get_pin_page_source(driver, url_pin)

            with open(filename, "w") as f:
                f.write(html)
                print(f"Saved HTML to {f.name}")
        except:
            print(f"Failed to save HTML of parcel page for PIN: {pin}")
    else:
        print(f"{filename} already exists")

def dupage_county_pins_list():
    df = pd.read_csv("./dupage_county.csv")
    return list(df["PIN"])

#def get_front_page_for_multiple_pins(pins_list):
#    for pin in pins_list:
#        time.sleep(1)
#        print("\n")
#        print("\n")
#        print(f"***** Scraping for PIN: {pin} *****")
#        get_front_parcel_page(pin)