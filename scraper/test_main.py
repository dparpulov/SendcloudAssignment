import pytest
import asyncio
import requests
import asyncio
from scraper.scrape import auto_update
from db import *


def test_show_all_items_check_status_code_equals_200():
    response = requests.get("http://127.0.0.1:8000/all_items")
    assert response.status_code == 200


def test_user_follows_check_status_code_equals_200():
    response = requests.get("http://127.0.0.1:8000/user/1/follows")
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "feeds_fail, expected",
    [
        ["https://guzvsadwa.com", "Auto update fail. Do it manually"],
        ["https://google.com", "Auto update fail. Do it manually"],
    ],
)
async def test_auto_update_fail(feeds_fail, expected):
    result = await asyncio.create_task(auto_update(None, feeds_fail))
    assert result == expected
