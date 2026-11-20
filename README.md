# FastAPI Blog

A small learning project with browser-friendly Jinja2 pages and a JSON API for
browsing blog posts.

## Run the application

From the project directory, start the development server:

```powershell
uv run uvicorn fastapi_blog.main:app --reload
```

You can also run the installed console command with `uv run fastapi-blog`.

Open `http://127.0.0.1:8000/` for the styled HTML page. FastAPI's interactive
JSON API documentation is available at `http://127.0.0.1:8000/docs`.

## Routes

| Method | URL | Response |
| --- | --- | --- |
| GET | `/` or `/posts` | HTML page listing every post |
| GET | `/posts/{post_id}` | HTML page for one post |
| GET | `/api/posts` | JSON array containing all posts |
| GET | `/api/posts/{post_id}` | JSON object for one post |
| GET | `/static/style.css` | Stylesheet used by the HTML pages |

The sample posts live in memory, so changes disappear when the server restarts.
`post_id` must be a positive integer; a valid but unknown ID returns HTTP 404.

## Concepts used

- **Path parameters:** `{post_id}` extracts a value from the URL. FastAPI parses
  it as an integer and `Path(gt=0)` rejects zero and negative values.
- **Pydantic models:** `Post` defines and validates the shape shared by the API
  and templates. `response_model` documents and serializes JSON responses.
- **Jinja2 templates:** HTML structure is separated from Python route logic.
  `TemplateResponse` passes data into templates, where Jinja escapes values.
- **Static files:** `StaticFiles` serves the CSS file independently of routes.
- **Exception handlers:** Validation errors return HTTP 422, expected HTTP
  errors keep their status (for example 404), and unexpected errors are logged
  and return a generic HTTP 500. `/api/...` routes get JSON errors; browser
  pages get a styled HTML error page.

## Learning the code

`src/fastapi_blog/main.py` contains the application setup, routes, and exception
handlers. `src/fastapi_blog/schemas.py` contains the shared Pydantic data
models. The package's `templates/` and `static/` folders hold the HTML views
and stylesheet. The root `main.py` remains as a compatibility entry point, so
`uv run uvicorn main:app --reload` also works.