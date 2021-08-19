import os
from scrape import *
import requests
from starlette.responses import JSONResponse
from scrape import UnavailableScrape
from fastapi import FastAPI
import sqlite3
from db import *
import asyncio
from models.feed import Feed


app = FastAPI()

# try:
#   os.remove("scraper.db")
# except OSError:
#     pass


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
    """
        This function runs on every start up
        It does the following things:
            - creates the connection
            - creates the cursor
            - creates all tables specified in db.py
            - populates the feeds table
            - populates the users table
            - creates the async background task which updates the feeds items
    """
    global connection
    connection = sqlite3.connect("scraper.db")
    connection.row_factory = sqlite3.Row
    global cursor
    cursor = connection.cursor()
    create_all_tables(cursor)
    add_feeds(cursor, feeds)
    add_users(cursor, 5)
    asyncio.create_task(auto_update(cursor, feeds))


@app.on_event("shutdown")
def shutdown_event():
    """
        This function stops the connection when the server process is stopped
    """
    connection.close()


@app.get("/")
async def root():
    """
        This function calls the get_feeds function and
        returns all the feeds from the db

        Args: 
            cursor: the db cursor
    """
    return get_feeds(cursor)


@app.post("/user/{user_id}/follow/feed/{feed_id}")
async def follow_feed_endpoint(user_id: int, feed_id: int):
    """
        This function calls the follow_feed function and
        returns a message depending on if it is successful

        Args:
        user_id (int): The id of the user that will follow a feed
        feed_id (int): The id of the feed that will be followed
    """
    if follow_feed(cursor, user_id, feed_id) != 0:
        return {f"User {user_id} now follows feed {feed_id}"}
    else:
        return {"Invalid user or feed"}


@app.post("/user/{user_id}/unfollow/feed/{feed_id}")
async def unfollow_feed_endpoint(user_id: int, feed_id: int):
    unfollow_feed(cursor, user_id, feed_id)
    return {f"User {user_id} unfollowed feed {feed_id}"}


@app.get("/user/{user_id}/follows")
async def user_following(user_id: int):
    return user_follows(cursor, user_id)


@app.get("/feed/{feed_id}/items")
async def show_feed_items(feed_id: int):
    return get_specific_feed_items(cursor, feed_id)


@app.post("/user/{user_id}/reads/item/{item_id}")
async def mark_read_item(user_id: int, item_id: int):
    if add_read_item(cursor, user_id, item_id) != 0:
        return {f"User {user_id} read article {item_id}"}
    else:
        return {"Ivalid user or no such article exists"}


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


@app.post("/update")
async def force_update_items():
    items = scrape_feeds(feeds)
    return update_items(cursor, items)


# @app.get("/load_feeds_users")
# async def load_default():
#     add_feeds(cursor, feeds)
#     add_users(cursor, 5)
#     return {"Feed and user tables populated"}


@app.get("/all_items")
async def show_all_items():
    return get_all_items(cursor)


@app.get("/feed/{feed_id}/items")
async def show_feed_items(feed_id: int):
    return get_specific_feed_items(cursor, feed_id)


@app.exception_handler(UnavailableScrape)
async def scraper_exception_handler(request: requests, exc: UnavailableScrape):
    return JSONResponse(
        status_code=418,
        content={
            "message": f"Oops! {exc.name} did something. Scraping doesn't work"},
    )
