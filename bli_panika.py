
import httplib2
import os
from bs4 import BeautifulSoup

baseurl = 'http://www.blipanika.co.il/?paged='
enc = 'utf-8'
dir = 'sipurim'


if not os.path.exists(dir):
    os.makedirs(dir)

h = httplib2.Http('.cache')

total_articles = 0
for i in range(84, 0, -1):
    url = baseurl + str(i)
    resp_headers, content = h.request(url, 'GET')
    soup = BeautifulSoup(content)
    links = soup.select('div.entry a[rel="bookmark"]')

    for uri in [link.get('href') for link in links]:
        total_articles += 1
        print('Fetching link #{} on {}.'.format(total_articles, uri))
        article_headers, article_content = h.request(uri)
        # Force the parcer to "html5lib". Default parser wont work
        article = BeautifulSoup(article_content, "html5lib", from_encoding=enc)

        try:
            entry = article.find('div', attrs={'class': 'entrytext'})
            text = entry.get_text()
            with open(os.path.join(dir, uri.split('p=')[1] + '.txt'), mode='w',
                      encoding=enc) as f:
                f.write(text)
        except AttributeError:
            print('Got parsing error.')
            with open('failed_links.txt', mode='a', encoding='utf-8') as f:
                f.write(uri + '\n')
