from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import random
import re
import datetime

# semente aleatoria
random.seed(datetime.datetime.now())

def getLinks(articleUrl):
    try:
       html = urlopen(f'http://en.wikipedia.org{articleUrl}')
    except HTTPError as e:
        print(f'Erro HTTP.. {e}')

        return False
    except URLError as e:
        print(f'Erro URL...{e}')
        return False
    else:
        bs = BeautifulSoup(html.read(), 'html.parser')
        try:
             content = bs.find('div',
                               {'id': 'bodyContent'})
             links = content.find_all('a',
                                      href=re.compile(r'^(/wiki/)((?!:).)*$'))
             return links
        except AttributeError as e:
             print(f'Erro atributo {e}')

             return False

links = getLinks('/wiki/Kevin_Bacon')

if not links:
    print('Fluxo parou com algum erro ....')
else:
    while len(links) > 0:
        newArticle = links[random.randint(0, len(links) - 1)].attrs['href']
        print(newArticle)
        links = getLinks(newArticle)
