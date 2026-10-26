---
title: app2 (FastAPI)
description: A tiny Python and FastAPI CRUD API for in-memory items.
---

# app2

Python + FastAPI. In-memory `items` CRUD; spec in `openapi.json`.
FastAPI also serves interactive docs at http://localhost:8000/docs.

Run alone:

```sh
uv run --with-requirements requirements.txt uvicorn main:app --port 8000
```

Under `docker compose up` (from the repo root), this folder is mounted and edits reload live.

To change dependencies, edit `requirements.txt` (pin exact versions), then
rebuild: `docker compose up --build -d app2`.

Or with Docker: `docker build -t app2 . && docker run -p 8000:8000 app2`.
