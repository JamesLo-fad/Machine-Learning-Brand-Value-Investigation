from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service

from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver import ActionChains
import re
import time
import pandas as pd
import mysql.connector
from gcloud import storage
import os



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
today = datetime.today()
current_date = today.strftime('%Y-%m-%d')
all_product = []
dict_list = []


s = Service(GeckoDriverManager().install())
options = webdriver.FirefoxOptions()

# s = Service(ChromeDriverManager().install())
# options = webdriver.ChromeOptions()

# options.add_argument("--headless")
# options.add_argument("--window-size=1920,1080")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-gpu")
# options.add_argument('--disable-dev-shm-usage')
# options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options, service=s)

########################################################################################################################################
for i in range(1,310):

    # driver.get(f"https://www.price.com.hk/category.php?c=100005&page={i}")
    driver.execute_script(f"location.href='https://www.price.com.hk/category.php?c=100005&page={i}';")
    time.sleep(10)
    print(i)
########################################################################################################################################
    webscrapping()
########################################################################################################################################

driver.close()


########################################################################################################################################
Price_mobile = pd.DataFrame.from_dict(dict_list, orient='columns')
Price_mobile.to_csv(f'Price_mobile_{current_date}.csv',index=False)
########################################################################################
os.environ.setdefault("GCLOUD_PROJECT", "arcane-grin-346209")
storage_client = storage.Client.from_service_account_json("arcane-grin-346209-822c6fb5d4ed.json")
bucket = storage_client.get_bucket('mobile_pricehk')
blob = bucket.blob(f'Price_mobile_{current_date}.csv')
blob.upload_from_filename(f'./Price_mobile_{current_date}.csv')
########################################################################################
