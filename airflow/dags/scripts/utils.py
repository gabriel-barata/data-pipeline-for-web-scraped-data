from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import math
import os
import re

#Scraping data
def scrape_data(url, table_name : str, increment : int = 37, results_per_page : int = 36):

    binary = FirefoxBinary('/usr/bin/firefox-esr')
    options = webdriver.FirefoxOptions()
    options.headless = True
    options.binary = binary
    
    driver = webdriver.Firefox(options=options, executable_path='/usr/local/bin/geckodriver')
    driver.get(url)

    nres = int(driver.find_element(By.XPATH, '//p[@class="pagination-total"]//strong').text)
    max_loads = math.floor(nres/results_per_page)

    for load in range(max_loads):
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'/html/body/main/div/section[1]/div/div/div[{str(increment)}]/button')))
        load_button = driver.find_element(By.XPATH, f'/html/body/main/div/section[1]/div/div/div[{str(increment)}]/button')
        load_button.send_keys(Keys.ENTER)
        increment += results_per_page

    data = pd.DataFrame()

    for div in driver.find_elements(By.XPATH, '//div[@class="showcase-item   js-event-product-click "]'):
        html = div.get_attribute('innerHTML')
        soup = BeautifulSoup(html)

        try:
            brand = soup.find('span', class_ = 'showcase-item-brand')
            product = soup.find('a', class_ = 'showcase-item-title')
            price = soup.find('span', class_ = 'price-value')
            descr = soup.find('p', class_ = 'showcase-item-description')

            brand = str(brand)
            product = str(product)
            price = str(price)
            descr = str(descr)

            temp_dict = {'brand' : brand,
                    'product' : product,
                    'price' : price,
                    'descr' : descr
            }

            temp = pd.DataFrame(temp_dict, index = [0])
            data = pd.concat([data, temp], axis = 0)

        except Exception as e:
            print(f"-failed to load div : {e}")

    driver.close()

    data.to_csv(f'opt/airflow/data/raw/{table_name}.csv')

    return 0

#Concatening the scraped data
def concat_data(table_name : str, path : str = '/opt/airflow/data/raw'):

    data = pd.DataFrame()
    files = os.listdir(path)

    for file in files:
        temp = pd.read_csv(path + file)
        data  = pd.concat([temp, data], axis = 0)

    data.to_csv(f'/opt/airflow/data/raw/{table_name}.csv')

    return 0

#Cleaning the scraped data
def clean_data(file_name, path : str = '/opt/airflow/data/raw/'):

    data = pd.read_csv(path + file_name + '.csv')

    for column in data.columns:
        data[str(column)] = data[str(column)].astype(str)
        data[str(column)] = data[str(column)].apply(lambda x : x.split('>')[1] if len(x.split('>')) > 1 else x)
        data[str(column)] = data[str(column)].apply(lambda x : x.split('<')[0] if len(x.split('<')) > 1 else x)
        data[str(column)] = data[str(column)].apply(lambda x : x.strip() if type(x) == str else x)

    data['volumetria'] = data['product'].apply(lambda x : x[-5:])
    data['volumetria'] = data['volumetria'].apply(lambda x : re.sub('^\D*', '', x))

    data['price'] = data['price'].apply(lambda x : x.replace('R$', ''))
    data['price'] = data['price'].apply(lambda x : x.replace('.', ''))
    data['price'] = data['price'].apply(lambda x : x.replace(',', '.'))
    data['price'] = data['price'].apply(lambda x : np.nan if x == 'None' else float(x))

    data['product'] = data['product'].apply(lambda x : x.split('-')[0] if len(x.split('-')) > 1 else x)

    for column in data.columns:
        data[str(column)] = data[str(column)].apply(lambda x : np.nan if x == 'None' else x)

    data['brand'] = data['brand'].apply(lambda x : x.upper())
    data['product'] = data['product'].apply(lambda x : x.upper())
    data['descr'] = data['descr'].apply(lambda x : x.upper())

    data['product'] = data['product'].apply(lambda x : x.replace(';', ''))

    cleaned_data = data[['product', 'brand', 'descr', 'price', 'vol']]
    
    cleaned_data.to_csv('/opt/airflow/data/staging/cleaned_data.csv')

    return 0