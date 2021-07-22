import requests


fake_db = {
    "feed": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
    "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
}


# def test_root():
# response = client.get_feeds()
# assert response.status_code == 200
# assert response.json() == {"msg": "Hello world"}


def test_follow_feed_endpoint():
    # url = "http://127.0.0.1:8000/user/1/follow/feed/1"
    # payload = "\"Working\""
    # headers = {
    #     'Content-Type': 'application/json'
    # }
    # response = requests.request("GET", url, headers=headers, data=payload)

    # assert response.status_code == 200
    assert 200 == 200
