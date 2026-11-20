"""A small FastAPI blog with browser pages and a JSON API."""

# Path builds asset locations relative to this installed package.
from pathlib import Path

# logging records unexpected server-side failures without exposing their details to clients.
import logging

# FastAPI builds the application; HTTPException represents expected HTTP failures.
from fastapi import FastAPI, HTTPException, Path as PathParameter, Request
# jsonable_encoder converts Pydantic validation details into JSON-safe values.
from fastapi.encoders import jsonable_encoder
# RequestValidationError is raised when client input does not match route requirements.
from fastapi.exceptions import RequestValidationError
# HTMLResponse sets the browser response content type; JSONResponse is used by API errors.
from fastapi.responses import HTMLResponse, JSONResponse, Response
# StaticFiles exposes the stylesheet to browsers.
from fastapi.staticfiles import StaticFiles
# StarletteHTTPException is the common base for FastAPI's HTTP exceptions and 404s.
from starlette.exceptions import HTTPException as StarletteHTTPException
# Jinja2Templates renders reusable HTML templates with escaped values.
from fastapi.templating import Jinja2Templates
# The shared schema defines and validates the shape of each blog post.
from .schemas import Post

# Keep templates and styles alongside the application so they are package resources.
BASE_DIR = Path(__file__).resolve().parent
# Configure a module logger so unexpected errors are visible in the server logs.
logger = logging.getLogger(__name__)

# Create the ASGI application that Uvicorn serves.
app = FastAPI(title="FastAPI Blog", description="A learning blog with HTML and JSON routes.")
# Serve the package's stylesheet at the /static URL path.
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
# Configure Jinja to load templates packaged with the application.
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# In-memory sample data keeps this beginner example independent of a database.
posts: list[Post] = [
    # Pydantic validates each sample record when it is created.
    Post(
        id=1,
        author="Corey Schafer",
        title="FastAPI is Awesome",
        content="This framework is really easy to use and super fast.",
        date_posted="April 20, 2025",
    ),
    # A second record makes both list and detail pages useful immediately.
    Post(
        id=2,
        author="Python Developer",
        title="Python and FastAPI",
        content="Python is a great language for web development, and FastAPI makes it even better.",
        date_posted="April 21, 2025",
    ),
]


# Keep the lookup in one helper so the HTML and JSON detail routes behave alike.
def find_post(post_id: int) -> Post:
    """Return one post or raise the standard 404 response when it does not exist."""

    # Search by the path identifier; the list is small, so a simple loop is sufficient.
    for post in posts:
        # Return the first record whose identifier matches the requested value.
        if post.id == post_id:
            return post
    # A missing record is a normal client-facing 404, not an unexpected server error.
    raise HTTPException(status_code=404, detail=f"Post {post_id} was not found.")


# These two URLs are aliases for the same browser-facing list page.
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
@app.get("/posts", response_class=HTMLResponse, include_in_schema=False)
def browse_posts(request: Request) -> HTMLResponse:
    """Render the browser page containing every post."""

    # TemplateResponse needs the Request for URL generation and template context.
    return templates.TemplateResponse(
        request=request,
        name="posts.html",
        # Passing the post list as context makes it available to the Jinja template.
        context={"posts": posts},
    )


# This route is for people browsing the site; it returns rendered HTML, not JSON.
@app.get("/posts/{post_id}", response_class=HTMLResponse, include_in_schema=False)
def post_page(
    request: Request,
    # Path(gt=0) rejects zero and negative IDs with FastAPI's standard 422 validation.
    post_id: int = PathParameter(gt=0, description="The positive ID of the post to display."),
) -> HTMLResponse:
    """Render one post as an HTML page."""

    # Reuse the same lookup logic as the JSON endpoint to keep 404 behavior consistent.
    post = find_post(post_id)
    # Render the selected record into the single-post template.
    return templates.TemplateResponse(
        request=request,
        name="post_detail.html",
        context={"post": post},
    )


# JSON routes stay in the OpenAPI schema so they appear in /docs.
@app.get("/api/posts", response_model=list[Post], summary="List all posts")
def get_posts() -> list[Post]:
    """Return every post as JSON."""

    # FastAPI serializes the declared Post models to the response JSON.
    return posts


# The API's detail route uses the same path ID and data lookup as the HTML route.
@app.get("/api/posts/{post_id}", response_model=Post, summary="Get one post")
def get_post(
    # FastAPI parses this path segment as an integer and validates it is positive.
    post_id: int = PathParameter(gt=0, description="The positive ID of the post to retrieve."),
) -> Post:
    """Return one post as JSON, selected by its path ID."""

    # The response model documents and validates the returned JSON structure.
    return find_post(post_id)


# Register handlers last so the route behavior is easy to read before error policy.
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> Response:
    """Return readable 422 errors in the same format as the requested interface."""

    # Convert validation errors to JSON-safe dictionaries for the API response.
    errors = jsonable_encoder(exc.errors())
    # Browser pages receive an HTML error page instead of raw JSON.
    if not request.url.path.startswith("/api/"):
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "status_code": 422,
                "message": "Some request data is invalid.",
                "errors": errors,
            },
            status_code=422,
        )
    # JSON clients receive FastAPI-style detail data and the conventional 422 status.
    return JSONResponse(status_code=422, content={"detail": errors})


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> Response:
    """Format expected HTTP errors as HTML for pages and JSON for API routes."""

    # API routes keep their normal JSON error shape for 404 and other HTTP errors.
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=exc.headers,
        )
    # Browser routes get a styled page while preserving the original status and headers.
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={
            "status_code": exc.status_code,
            "message": str(exc.detail),
            "errors": [],
        },
        status_code=exc.status_code,
        headers=exc.headers,
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> Response:
    """Log unexpected failures and return a safe generic 500 response."""

    # Keep the traceback in server logs for debugging; do not reveal internals to clients.
    logger.exception("Unexpected error while handling %s", request.url.path, exc_info=exc)
    # HTML callers get a friendly error page without implementation details.
    if not request.url.path.startswith("/api/"):
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "status_code": 500,
                "message": "An unexpected server error occurred.",
                "errors": [],
            },
            status_code=500,
        )
    # API callers get a stable JSON shape without sensitive exception details.
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected server error occurred."},
    )


def main() -> None:
    """Run the development server when the installed `fastapi-blog` command is used."""

    import uvicorn

    uvicorn.run("fastapi_blog.main:app", host="127.0.0.1", port=8000)
