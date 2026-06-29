from pydantic import BaseModel


class Post(BaseModel):
    """Schema of a /posts item.

    Constructing ``Post(**item)`` validates types and required fields
    declaratively. A missing or mistyped field raises ValidationError, which is
    a stronger contract check than a handful of ``assert "id" in item``.
    """

    userId: int
    id: int
    title: str
    body: str
