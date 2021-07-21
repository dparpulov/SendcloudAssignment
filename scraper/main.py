from fastapi import FastAPI
import sqlite3
import os
from scrape import srape
from db import *

app = FastAPI()

try:
    os.remove("scraper.db")
except OSError:
    pass


connection = ...
cursor = ...

feeds = [
    "http://www.nu.nl/rss/Algemeen",
    "https://feeds.feedburner.com/tweakers/mixed",
    "https://news.ycombinator.com/rss",
    "https://feeds.simplecast.com/54nAGcIl",
]


@app.on_event("startup")
def startup_event():
    global connection
    connection = sqlite3.connect("scraper.db")
    connection.row_factory = sqlite3.Row
    global cursor
    cursor = connection.cursor()
    create_all_tables(cursor)


@app.on_event("shutdown")
def shutdown_event():
    connection.close()


@app.get("/")
async def root():
    return get_feeds(cursor)


@app.get("/user/{user_id}/follow/feed/{feed_id}")
async def follow_feed_api(user_id: int, feed_id: int):
    follow_feed(cursor, user_id, feed_id)
    return {f"User {user_id} now follows feed {feed_id}"}


@app.get("/user/{user_id}/unfollow/feed/{feed_id}")
async def unfollow_feed_api(user_id: int, feed_id: int):
    unfollow_feed(cursor, user_id, feed_id)
    return {f"User {user_id} unfollowed feed {feed_id}"}


@app.get("/following/{user_id}")
async def user_following(user_id: int):
    return user_follows(cursor, user_id)


@app.get("/load_default")
async def load_default():
    add_feeds(cursor, feeds)
    add_users(cursor, 5)
    return {"Feed and user tables populated"}
