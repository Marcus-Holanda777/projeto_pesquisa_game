from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import requests
import os
import shutil
import pandas as pd

def imgCarrega(link, pasta):
    if not link.lower().endswith('.png') and not link.lower().endswith('.jpg'):
        link = link + '.jpg'

    if link.startswith('https'):
       res = requests.get(f'{link}')
    else:
       res = requests.get(f'https:{link}')

    nm_file = os.path.join(pasta, '-'.join(link.split('/')[1:]))
    img_gile = open(nm_file, 'wb')

    for chunk in res.iter_content(100000):
        img_gile.write(chunk)
    img_gile.close()


def baixaImg(dados, pasta):
    if os.path.isdir(pasta):
        shutil.rmtree(pasta)
    os.mkdir(pasta)

    for marca in dados:
        if marca['Img']== '':
            pass
        else:
           imgCarrega(marca['Img'], pasta)


def marcas(site):
    base = {}
    completo = []

    try:
        html = urlopen(f'{site}/marcas')
    except HTTPError as e:
        print(e)
    else:
        bs = BeautifulSoup(html.read(), 'html.parser')
        tabela = bs.find('table', {'class': 'listTable brandTable'})

        for x in tabela.find_all('tr'):
            if x.span != None:
                base['Img'] = x.find('span', {'class': 'tableImg'}).img.attrs['data-src']
                base['Modelo'] = x.find('span', {'class': 'tableTitle'}).getText()
                base['Qtd'] = x.find('span', {'class': 'tableText'}).getText()
                base['Link_marca'] = x.find('span', {'class': 'tableImg'}).a.attrs['href']

                completo.append(base.copy())

    return completo


def salvarDados(dados):
    pd.DataFrame(dados).to_excel('Carros.xlsx', index=False)


def carros(site, dados):
    base = {}
    completo = []

    for link_int in dados:
        try:
            html = urlopen(f'{site}{link_int["Link_marca"]}')
        except HTTPError as e:
            print(e)
        else:
            bs = BeautifulSoup(html.read(), 'html.parser')
            tabela = bs.find('table', {'class': 'listTable carTable'})

            for x in tabela.find_all('tr'):
                if x.span != None:
                    base['Img'] = x.find('span', {'class': 'tableImg'}).img.attrs['data-src']
                    base['Modelo'] = x.find('span', {'class': 'tableTitle'}).getText()
                    base['Categoria'] = x.find('span', {'class': 'tableText'}).getText()
                    base['Link_marca'] = link_int["Link_marca"]
                    base['Link_carro'] = x.find('span', {'class': 'tableImg'}).a.attrs['href']

                    completo.append(base.copy())

    return completo



SITE = 'https://www.kbb.com.br'
MARCA = marcas(SITE)
baixaImg(MARCA, 'img-marcas')

CARRO = carros(SITE, MARCA)
baixaImg(CARRO, 'img-carros')

salvarDados(CARRO)