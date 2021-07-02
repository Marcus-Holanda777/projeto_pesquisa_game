import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

def formatPreco(preco):
    preco = preco.replace('R$\xa0', '')
    preco = preco.replace('.', '')
    preco = preco.replace(',', '.')

    return preco

def termo_de_pesquisa(pesquisa):
    '''
        digitar o produto que deseja pesquisar
    '''
    template = 'https://www.amazon.com.br/s?k={}'
    pesquisa = pesquisa.replace(' ', '+')

    url = template.format(pesquisa)

    url += '&page={}'

    return url


def extrairRegistros(item):
    nome = item.h2.a
    nome_h2 = nome.get_text().strip()
    url_int = 'https://www.amazon.com.br' + nome.attrs['href']

    # preco
    try:
        tag_price = item.find('span', 'a-price')
        tag_price = tag_price.find('span', 'a-offscreen').get_text().strip()
    except AttributeError:
        return

    try:
        pontos = item.i.get_text().strip()
        #avalia = item.find('span', {'class': 'a-size-base', 'dir': 'auto'})

        avalia = item.select_one('span[class="a-size-base"]').get_text().strip()
    except AttributeError:
        pontos = ''
        avalia = ''

    result = (nome_h2, url_int, tag_price, pontos, avalia)

    return result


# driver do firefox
total = []
driver = webdriver.Firefox()
url = termo_de_pesquisa('console ps4')

for page in range(1, 21):
    driver.get(url.format(page))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    resultado = soup.find_all('div', {'data-component-type': 's-search-result'})

    for item in resultado:
        registro = extrairRegistros(item)
        if registro:
           total.append(registro)

driver.close()

colunas = ['Nome', 'Link', 'Preco', 'Estrelas', 'Classificacao']
saida = pd.DataFrame(total, columns=colunas)
saida.loc[0:, 'Preco'] = saida['Preco'].map(formatPreco)

saida['Preco'] = saida['Preco'].astype(float)
saida.to_excel('Saida.xlsx', index=False)


#with open('saida.csv', 'w', newline='', encoding='utf-8') as save:
#    escrever = csv.writer(save)
#    escrever.writerows(total)


