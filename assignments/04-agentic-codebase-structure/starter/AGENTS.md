# Repository Guide

## Purpose

This repository contains a tiny FastAPI + SQLite link shortener. Clients can
create short links with `POST /shorten` and follow them with `GET /{code}`.

## Important files

- `main.py` — API routes, validation, SQLite setup, and short-code generation.
- `test_main.py` — starter API tests.
- `tests/` — additional behavioral tests and test-specific guidance.
- `docs/TASKS.md` — the small feature tasks for this exercise.
- `.agents/skills/implement-feature/SKILL.md` — reusable feature workflow.

## Install, run, and test

```bash
pip install -r requirements.txt
pytest
uvicorn main:app --reload
```

The development server is available at `http://localhost:8000`; interactive
API documentation is at `/docs`. The SQLite file `links.db` is local runtime
state and should not be committed.

## Product boundaries

Keep this service focused on URL shortening, redirect behavior, and small
link-management features. Do not add authentication, analytics, a frontend,
external services, or a new persistence layer for this exercise.

## Change workflow

Understand the selected task and existing behavior, run the tests, add a
behavioral test, implement the smallest compatible change, then run `pytest`
again and summarize any remaining risks.
