from fastapi import FastAPI
import sqlite3
import os
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


@app.get("/feed/{feed_id}/items")
async def show_feed_items(feed_id: int):
    return get_specific_feed_items(cursor, feed_id)


@app.get("/user/{user_id}/reads/item/{item_id}")
async def mark_read_item(user_id: int, item_id: int):
    return add_read_item(cursor, user_id, item_id)


@app.get("/user/{user_id}/show_read")
async def read_items_global(user_id: int):
    return show_all_read_items(cursor, user_id)


@app.get("/user/{user_id}/show_unread")
async def unread_items_global(user_id: int):
    return show_all_unread_items(cursor, user_id)


@app.get("/user/{user_id}/show_read/feed/{feed_id}")
async def read_items_feed(user_id: int, feed_id: int):
    return show_read_items_feed(cursor, user_id, feed_id)


@app.get("/user/{user_id}/show_unread/feed/{feed_id}")
async def unread_items_feed(user_id: int, feed_id: int):
    return show_unread_items_feed(cursor, user_id, feed_id)


@app.get("/update")
async def force_update_items():
    return update_items(cursor)


@app.get("/load_feeds_users")
async def load_default():
    add_feeds(cursor, feeds)
    add_users(cursor, 5)
    return {"Feed and user tables populated"}


@app.get("/all_items")
async def show_all_items():
    return get_all_items(cursor)


@app.get("/feed/{feed_id}/items")
async def show_feed_items(feed_id: int):
    return get_specific_feed_items(cursor, feed_id)
