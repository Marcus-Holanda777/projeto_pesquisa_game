import re



compilador = re.compile(r'\d.*,\d{2}')
ret = compilador.search('R$ \n\n\n116,92 \n\n\n\n '
                        ''
                        'a vista')
print(ret.group())