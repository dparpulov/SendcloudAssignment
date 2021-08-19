from pydantic import BaseModel


class Feed_item(BaseModel):
    _id: int
    title: str
    item_url: str
    published: str
    feed_url: str
