from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import pandas as pd
import math
import os

def scrape_data(url, increment : int = 37, results_per_page):

    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
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
            preco_inicial = soup.find('div', class_ = 'item-price-max')
            preco_aplicado = soup.find('span', class_ = 'price-value')
            vegano = soup.find('span', class_ ='showcase-label-dynamic showcase-label-vegano')
            descricao = soup.find('p', class_ = 'showcase-item-description')
            novidade = soup.find('span', class_ = 'showcase-label-dynamic showcase-label-novidade')
            cruelty_free = soup.find('span', class_ = 'showcase-label-dynamic showcase-label-cruelty-free')

            marca = str(marca)
            produto = str(produto)
            preco_inicial = str(preco_inicial)
            preco_aplicado = str(preco_aplicado)
            vegano = str(vegano)
            descricao = str(descricao)
            novidade = str(novidade)
            cruelty_free = str(cruelty_free)

            temp_dict = {'marca' : marca,
                    'produto' : produto,
                    'preco_inicial' : preco_inicial,
                    'preco_aplicado' : preco_aplicado,
                    'descricao' : descricao,
                    'vegano' : vegano,
                    'cruelty_free' : cruelty_free,
                    'novidade' : novidade}

            temp = pd.DataFrame(temp_dict, index = [0])
            raw_data = pd.concat([raw_data, temp], axis = 0)

        except Exception as e:
            print(f"FALHA AO CARREGAR DIV : {e}")

    driver.close()

    raw_data.to_csv('opt/airflow/data/raw_data.csv')~

    return 0