# Link Shortener — Assignment 04

A small FastAPI + SQLite service that creates short links and redirects users
to their original URLs. This version implements the **custom alias** task:
clients may request a readable alias, and a duplicate alias returns `409`.

## Setup

```bash
pip install -r requirements.txt
pytest
uvicorn main:app --reload
```

Try it with `POST /shorten`:

```json
{"url": "https://example.com/docs", "alias": "docs"}
```

The response is `{"code":"docs","short_url":"/docs"}`. A second request
using `docs` returns `409`. Aliases may contain letters, numbers, hyphens, and
underscores.
