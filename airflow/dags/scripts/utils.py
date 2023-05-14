from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
import geckodriver_autoinstaller
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import pandas as pd
import math
import os

def scrape_data(url, increment : int = 37, results_per_page : int = 36):

    binary = FirefoxBinary('/var/lib/flatpak/app/org.mozilla.firefox/x86_64/stable/3d0b2ca2b49b01730902343cbce5960f0ab5d212b1076cf3d11d543d2b3fd1bf/files/bin/firefox')
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

    raw_data = pd.DataFrame()

    for div in driver.find_elements(By.XPATH, '//div[@class="showcase-item   js-event-product-click "]'):
        html = div.get_attribute('innerHTML')
        soup = BeautifulSoup(html)

        try:
            marca = soup.find('span', class_ = 'showcase-item-brand')
            produto = soup.find('a', class_ = 'showcase-item-title')
            preco = soup.find('span', class_ = 'price-value')
            descricao = soup.find('p', class_ = 'showcase-item-description')

            marca = str(marca)
            produto = str(produto)
            preco_inicial = str(preco_inicial)
            preco = str(preco)
            descricao = str(descricao)

            temp_dict = {'marca' : marca,
                    'produto' : produto,
                    'preco_inicial' : preco_inicial,
                    'preco' : preco,
                    'descricao' : descricao
            }

            temp = pd.DataFrame(temp_dict, index = [0])
            raw_data = pd.concat([raw_data, temp], axis = 0)

        except Exception as e:
            print(f"FALHA AO CARREGAR DIV : {e}")

    driver.close()

    raw_data.to_csv('opt/airflow/data/raw_data.csv')

    return 0