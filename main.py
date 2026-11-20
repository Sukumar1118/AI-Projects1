"""Compatibility entry point for running the blog from the project root."""

# Keep `uvicorn main:app` working while the application lives in the package.
from fastapi_blog.main import app

__all__ = ["app"]
