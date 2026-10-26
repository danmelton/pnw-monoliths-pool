---
title: App pool
description: Two tiny sample CRUD apps, one TypeScript and one Python, run together with Docker Compose.
---

# app-pool

Two sample apps with the same in-memory `items` CRUD API:

- `app1/`: TypeScript + Express, on http://localhost:3000
- `app2/`: Python + FastAPI, on http://localhost:8000

Each app has its API spec in `openapi.json`.

## Install Docker

**Mac:** install [OrbStack](https://orbstack.dev) (`brew install orbstack`) or
[Docker Desktop](https://www.docker.com/products/docker-desktop/). Either one
provides `docker compose`. Open the app once after installing.

**Windows:** install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
with the WSL 2 backend (OrbStack is Mac-only).

- If WSL isn't set up, run `wsl --install` in an admin PowerShell and restart.
- Clone this repo inside WSL (e.g. `~/code` in Ubuntu), not on `C:\`. Folders on
  the Windows drive may not pass file-change events into containers, so live
  reload wouldn't work.
- Step-by-step guides:
  - [Install Docker Desktop on Windows](https://docs.docker.com/desktop/setup/install/windows-install/) (Docker)
  - [Docker Desktop and WSL 2](https://docs.docker.com/desktop/features/wsl/) (Docker)
  - [WSL best practices](https://docs.docker.com/desktop/features/wsl/best-practices/) (Docker; why to keep code inside WSL)
  - [Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install) (Microsoft)

**Check it works:** `docker --version` and `docker compose version`.

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

Each app's code is mounted into its container, so edits reload live (no rebuild).

Stop with `docker compose down`.

## Changed dependencies?

Dependencies don't reload live; they're baked into each image. After changing
`app1/package.json` or `app2/requirements.txt`, rebuild that app:

```sh
docker compose up --build -d app1   # or app2
docker compose up --build           # both
```
