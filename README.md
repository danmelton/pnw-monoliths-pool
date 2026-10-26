---
title: App pool
description: Two tiny sample CRUD apps, one TypeScript and one Python, run together with Docker Compose.
---

# app-pool

Two sample apps with the same in-memory `items` CRUD API:

- `app1/`: TypeScript + Express, on http://localhost:3000
- `app2/`: Python + FastAPI, on http://localhost:8000

Each app has its API spec in `openapi.json`.

## Run

```sh
docker compose up --build
```

Try it:

```sh
curl -X POST localhost:3000/items -H 'Content-Type: application/json' -d '{"name":"apple"}'
curl localhost:3000/items
```

Routes (both apps): `GET /items`, `POST /items`, `GET /items/{id}`, `PUT /items/{id}`, `DELETE /items/{id}`.

Stop with `docker compose down`.
