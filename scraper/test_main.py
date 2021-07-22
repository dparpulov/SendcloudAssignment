import pytest
import asyncio
import requests
import asyncio
from scraper.scrape import auto_update
from db import *

# def test_root():
# response = client.get_feeds()
# assert response.status_code == 200
# assert response.json() == {"msg": "Hello world"}


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
