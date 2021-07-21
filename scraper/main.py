from scrape import srape
from fastapi import FastAPI

app = FastAPI()

feeds = [
    "http://www.nu.nl/rss/Algemeen",
    "https://feeds.feedburner.com/tweakers/mixed",
    "https://news.ycombinator.com/rss",
    "https://feeds.simplecast.com/54nAGcIl",
]


@app.get("/")
async def root():
    return srape(feeds)
