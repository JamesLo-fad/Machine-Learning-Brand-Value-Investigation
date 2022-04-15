from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver import ActionChains
import time
import pandas as pd
# import mysql.connector
# from gcloud import storage
# import os
# import re

########################################################################################
def webscrapping():
    mobile_menu = driver.find_element(By.CSS_SELECTOR, '.list-product-list')
    for element in mobile_menu.find_elements(By.CSS_SELECTOR, '.item-inner'):
        temp = []
        temp_02 = []
        dict_product = {}
        mobile_title = element.find_element(By.CSS_SELECTOR, ".line-01").text
        mobile_price = element.find_elements(By.CSS_SELECTOR, ".text-price-number")
        if len(mobile_price) < 1:
            break
        else:
            mobile_price = mobile_price[0].text.replace(",", "")
        dict_product["名稱"] = mobile_title
        dict_product["價格"] = mobile_price
        ########################################################################################################################################
        mobile_spec_menu = element.find_element(By.CSS_SELECTOR, ".line-04")
        for attr in mobile_spec_menu.find_elements(By.CSS_SELECTOR, ".item-attr"):
            for item in attr.find_elements(By.TAG_NAME, "tr"):
                spec_title = item.find_element(By.CSS_SELECTOR, ".attr-label").text.strip(":")
                spec_param = item.find_element(By.CSS_SELECTOR, ".attr-info").text
                if "天璣" in spec_param:

                    spec_param = spec_param.replace("天璣","MediaTek")
                    spec_param = "".join(set(spec_param))

                dict_product[spec_title] = spec_param
        dict_list.append(dict_product)


########################################################################################
all_product = []
dict_list = []
today = datetime.today()
current_date = today.strftime('%Y-%m-%d')

s = Service(GeckoDriverManager().install())
options = webdriver.FirefoxOptions()

# options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-gpu")
# options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Firefox(options=options,service=s)

########################################################################################################################################
driver.get("https://www.price.com.hk/category.php?c=100005&page=1")
time.sleep(5)

while True:
########################################################################################################################################
    webscrapping()
########################################################################################################################################
    last_page = int(driver.find_element(By.CSS_SELECTOR,'.pagination-wrapper .pagination li:nth-child(8)').get_attribute("textContent"))
    current_page = int(driver.find_element(By.CSS_SELECTOR,'.pagination-wrapper .pagination .active').get_attribute("textContent"))
    print(current_page)
    if last_page == current_page:
       break
    next_page = driver.find_element(By.CSS_SELECTOR, '.next-btn a[href*="category"]')
    driver.execute_script("arguments[0].scrollIntoView();", next_page)
    time.sleep(5)
    next_page.click()
########################################################################################################################################
    ads_elems = driver.find_elements(By.CSS_SELECTOR, ".adsbygoogle.adsbygoogle-noablate[data-vignette-loaded=true]")
    if len(ads_elems) > 0:
        ActionChains(driver).move_by_offset(5, 5).click().perform()
        time.sleep(5)

driver.close()

Price_mobile = pd.DataFrame.from_dict(dict_list, orient='columns')
Price_mobile.to_csv(f'Price_mobile_{current_date}.csv',index=False)
########################################################################################

