from pydantic import BaseModel


class Feed(BaseModel):
    _id: int
    url: str
