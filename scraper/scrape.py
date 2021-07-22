import asyncio
from db import update_items
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

    items = [tuple(item.values()) for item in items]

    return items


async def auto_update(cursor, feeds):
    """
        This function tries to update the feed items periodically

        Every 3 failed attempts the system notifies the user with a sound
        and a manual update is required
    """
    fail_attempts = 0

    while True:
        try:
            if fail_attempts < 3:
                print("Update INCOMIIIING!!!!!")
                items = scrape_feeds(feeds)
                if cursor:  # testing purposes, when cursor is empty, a test without a db is running
                    update_items(cursor, items)
                await asyncio.sleep(10)
        except:
            fail_attempts += 1
            print(f"Number of fails: {fail_attempts}")
            await asyncio.sleep(3)
            if fail_attempts == 3:
                return "Auto update fail. Do it manually"
