from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import pandas as pd
import re

driver = webdriver.Firefox()
driver.implicitly_wait(10)


lista_total = []


class Conteudo:
    def __init__(self, url, titulo, preco):
        self.url = url
        self.titulo = titulo
        self.preco = preco

    def formatPreco(self, preco):
        compilador = re.compile(r'\d.*,\d{2}')

        preco = compilador.search(preco).group()
        preco = preco.replace('.', '')
        preco = preco.replace(',', '.')

        return float(preco)

    def adicionar(self):
        lista_total.append(
            (self.titulo, self.url, self.formatPreco(self.preco)))


class WebSite:
    '''
        Contem informacoes sobre a estrutura do site
    '''

    def __init__(self, nome, url, tagbox, taglink, tagtitulo, tagpreco):
        self.nome = nome
        self.url = url
        self.tagbox = tagbox
        self.taglink = taglink
        self.tagtitulo = tagtitulo
        self.tagpreco = tagpreco


class Crawler:
    def getPage(self, url):
        try:
            driver.get(url)
        except WebDriverException:
            return None
        return BeautifulSoup(driver.page_source, 'html.parser')

    def safeGet(self, pageObj, selector):
        selectedElems = pageObj.select(selector)
        if selectedElems is not None and len(selectedElems) > 0:
            return selectedElems
        else:
            return ''

    def parse(self, site, url):

        bs = self.getPage(url)
        if bs is not None:
            boxs = self.safeGet(bs, site.tagbox)
            for box in boxs:
                try:
                    link = self.safeGet(box, site.taglink)[0].get('href')
                except IndexError:
                    link = '/proximo'
                if not link.startswith('https'):
                    link = f'{site.url}{link}'

                try:
                    titulo = self.safeGet(box, site.tagtitulo)[
                        0].get_text().strip()
                except IndexError:
                    titulo = 'nada'

                try:
                    preco = self.safeGet(box, site.tagpreco)[
                        0].get_text().strip()
                except IndexError:
                    preco = '0,99'

                _cont = Conteudo(link, titulo, preco)
                _cont.adicionar()


cr_ler = Crawler()
sites_dados = [['Extra', 'https://www.extra.com.br', 'ul[class*="ProductsGrid"] li', 'a', 'p[class*="ProductCard__Title"]', 'span[class*="ProductPrice__PriceValue"]'],
               ['Amazon', 'https://www.amazon.com.br',
                'div[data-component-type="s-search-result"]', 'h2 a',
                'h2 a', 'span[class="a-price"] span[class="a-offscreen"]'],
               ['Casas Bahia', 'https://www.casasbahia.com.br', 'ul[class*="ProductsGrid"] li',
                   'a', 'p[class*="ProductCard__Title"]', 'span[class*="ProductPrice__PriceValue"]'],
               ['Americanas', 'https://www.americanas.com.br',
                'div[class*="src__ColGridItem"]',
                'a', 'span[class*="src__Name"]', 'span[class*="src__PromotionalPrice"]'],
               ['Magazine luiza', 'https://www.magazineluiza.com.br',
                'ul.productShowCase li',
                'a', 'h3', 'span.price']]

websites = []
for row in sites_dados:
    websites.append(WebSite(row[0], row[1], row[2], row[3], row[4], row[5]))


cr_ler.parse(websites[0], 'https://m.extra.com.br/console-ps4/b')
cr_ler.parse(websites[1], 'https://www.amazon.com.br/s?k=console+ps4')
cr_ler.parse(websites[2], 'https://www.casasbahia.com.br/console-ps4/b')
cr_ler.parse(websites[3], 'https://www.americanas.com.br/busca/console-ps4')
cr_ler.parse(
    websites[4], 'https://www.magazineluiza.com.br/busca/console%20ps4')

driver.quit()

colunas = ['nome', 'url', 'preco']
saida = pd.DataFrame(lista_total, columns=colunas)
saida = saida[saida['preco'] > 999]
saida = saida[saida['nome'].str.startswith('Console')].sort_values(['preco'])

print(f'Menor preco: {saida["preco"].min()}')
print(f'Maior preco: {saida["preco"].max()}')
print(f'Mediana preco: {saida["preco"].median()}')
print(f'Media preco: {saida["preco"].mean():.2f}\n\n')

for row in saida.itertuples():
    print(f'NOME: {row.nome}\nURL: {row.url}\nPRECO: {row.preco}\n')


saida.to_excel('Saida.xlsx', index=False)
