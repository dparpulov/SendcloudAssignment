import requests
from bs4 import BeautifulSoup
from datetime import datetime


class UnavailableScrape(Exception):
    def __init__(self, name: str):
        self.name = name


def scrape_feeds(feeds):
    """
        This function iterates over the feed urls and scrapes each item using BS

        Args:
            feeds (list): A list of feed urls for scraping

        Returns:
            list: The return value is a list of all scraped items

        Raises:
            UnavailableScrape: if there are no scraped items at the end
    """
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
    if len(items) == 0:
        raise UnavailableScrape("No items found in the given url")

    return items
