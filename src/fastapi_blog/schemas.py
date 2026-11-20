"""Pydantic models that define and validate the blog's data."""

from pydantic import BaseModel


class Post(BaseModel):
    """The validated data shape shared by HTML pages and JSON responses."""

    # Identifies the post and appears in its URL path.
    id: int
    # Names the person who wrote the post.
    author: str
    # Provides the short heading shown in post lists.
    title: str
    # Stores the full text shown on the post detail page.
    content: str
    # Displays the publication date in the sample's readable format.
    date_posted: str
