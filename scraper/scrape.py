import requests
from bs4 import BeautifulSoup
from datetime import datetime


def srape(feeds):
    items = []
    for url in feeds:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, features='xml')

        for i in soup.findAll('item'):
            title = i.find('title').text
            link = i.find('link').text
            date_string = i.find('pubDate').text
            try:
                published = datetime.strptime(
                    date_string, '%a, %d %b %Y %H:%M:%S %z'
                )
            except ValueError:
                published = datetime.strptime(
                    date_string, '%a, %d %b %Y %H:%M:%S %Z'
                )
            item = {
                'title': title,
                'item_url': link,
                'published': published,
                'feed_url': url,
            }
            items.append(item)
    return items
