import requests
from bs4 import BeautifulSoup

def formatPreco(preco):
    preco = preco.replace('R$', '')
    preco = preco.replace('.', '')
    preco = preco.replace(',', '.')

    return float(preco)

def produto(site, link_interno, cab):
    #allow_redirects = True
    session = requests.Session()

    #print(f'{site}{link_interno}')
    html = session.get(f'{site}{link_interno}', headers=cab, allow_redirects=True)
    bs = BeautifulSoup(html.content, 'html.parser')

    print(bs)

    try:
        #priceblock_ourprice
        nome = bs.find('span', {'id': 'productTitle'}).get_text().strip()
        preco = formatPreco(bs.find('span', {'id': 'priceblock_ourprice'}).get_text().strip())
        link = f'{site}{link_interno}'
    except Exception as e:
        return tuple()
    else:
        return {'Produto': nome, 'Preco': preco, 'Link': link}

site_base = 'https://www.amazon.com.br'
site = 'https://www.amazon.com.br/s?k=console+nintendo+switch'

#cab = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
#       'Upgrade-Insecure-Requests': '1', 'x-runtime': '148ms'}

cab = {'User-Agent': 'Mozila/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
       'AppleWebKit 537.36 (KHTML, like Gecho) Chome',
       'Accept': 'text/html,application/xhtml+xml,application/xml;'
       'q=0.9,image/webp,*/*;q=0.8'}

session = requests.Session()
html = session.get(site, headers=cab, allow_redirects=True)
bs = BeautifulSoup(html.content, 'html.parser')
link_interno = set()
preco = set()


for a_link in bs.find_all('a'):
    if 'href' in a_link.attrs:
        if a_link.attrs['href'].lower().startswith('/console'):
             if a_link.attrs['href'] not in link_interno:
                link_interno.add(a_link.attrs['href'])

print(f'Qtd link {len(link_interno)}')
for x in link_interno:
    entrada = produto(site_base, x, cab)
    if len(entrada) > 0:
        if entrada['Preco'] not in preco:
           preco.add(entrada['Preco'])
    break

