from selenium import webdriver
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import os
import shutil
from datetime import datetime

url = 'https://m.extra.com.br/console-nintendo-switch/b'

driver = webdriver.Firefox()
driver.implicitly_wait(10)
driver.get(url)

bs = BeautifulSoup(driver.page_source, 'html.parser')
ul_bs = bs.find('ul', class_=re.compile('ProductsGrid'))

dados = []
registro = dict()

if os.path.isdir('extra-img'):
     shutil.rmtree('extra-img')
     os.mkdir('extra-img')
else:
    os.mkdir('extra-img')


cont = 1
for x in ul_bs.find_all('li'):
     registro['link'] = x.find('a').attrs['href']
     registro['preco'] = x.find('span',
                                class_=re.compile('ProductPrice__PriceValue')).get_text()
     registro['nome'] = x.find('p',
                               class_=re.compile('ProductCard__Title')).get_text()
     url_img = x.find('img').attrs['src']

     caminho= os.path.join('extra-img', str(cont) + '_.png')

     img_save = driver.find_element_by_xpath(f'//img[@src="{url_img}"]')
     driver.execute_script('arguments[0].scrollIntoView({block: "center", inline: "center"})', img_save)

     time.sleep(0.5)
     img_save.screenshot(caminho)


     registro['caminho'] = caminho
     registro['Data'] = datetime.now()
     dados.append(registro.copy())

     cont += 1

saida = pd.DataFrame(dados)
saida.loc[0:, 'preco'] = saida['preco'].map(lambda x: x.replace('R$ ', '').replace('.', '').replace(',', '.'))
saida.loc[0:, 'preco'] = saida['preco'].astype(float)

saida.to_excel('Saida.xlsx', index=False)
