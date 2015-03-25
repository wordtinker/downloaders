#
# Simple script to download pdf files from site.
#
#

import httplib2
import os
from bs4 import BeautifulSoup

baseurl = 'http://sefer-li.net/'
url = 'http://sefer-li.net/agada.htm'
enc = 'ISO-8859-1'
dir = 'pdfs'

h = httplib2.Http('.cache')
resp_headers, content = h.request(url, 'GET')
content = content.decode(enc)

soup = BeautifulSoup(content)
links = soup.find_all('a')
length = len(links)
print('Found {} links.'.format(length))

if not os.path.exists(dir):
    os.makedirs(dir)

for i, link in enumerate(links):
    print('Fetching link #{} of {}.'.format(i + 1, length))
    href = link.get('href')
    if href.endswith('.pdf'):
        resp_headers, content = h.request(baseurl + href)
        with open(os.path.join(dir, href), mode='wb') as f:
            f.write(content)
    else:
        with open('links.txt', mode='a', encoding='utf-8') as f:
            f.write(href + '\n')


### console comand to convert pdfs to txt
### for file in *.pdf; do pdftotext -enc UTF-8 "$file"; done ###
