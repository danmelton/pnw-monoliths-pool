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

Or with Docker: `docker build -t app2 . && docker run -p 8000:8000 app2`.
