import time
import ccxt
import requests
from selenium import webdriver


def cal_DOT(present, TRX, BTC, USDT, USDC, BTC_price):
    return (present-USDC-USDT-BTC*BTC_price)/TRX


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

url = 'https://tdr.org/'
driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=options)
driver.implicitly_wait(time_to_wait=5)

driver.get(url)
transparency = driver.find_element_by_css_selector('.transparency .issuance-wrap b').text
#time.sleep(3)
collateral_value = driver.find_elements_by_css_selector('.tokenList .value')
        #collateral_token = driver.find_elements_by_css_selector('.tokenList .label')
        #time.sleep(3)
transparency = transparency.split()
#print("present : {}".format(transparency[1]))
collateral = [k.text.replace(',', '') for k in collateral_value]
        #col_token = [k.text for k in collateral_token]
total = transparency[1].replace(',', '')
cols = ' '.join(collateral)
    
with open('tdr.txt', 'w', encoding='utf-8') as f:
    f.writelines(total+'\n')
    f.writelines(cols)


driver.close()