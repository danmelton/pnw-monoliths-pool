---
title: PNW Monolith app pool
description: A docker setup for our cutsie patootsie (micro) services.
---

# app-pool

Two sample apps with the same `items` CRUD API:

- `app1/`: TypeScript + Express, on http://localhost:3000
- `app2/`: Python + FastAPI, on http://localhost:8000

Each app has its API spec in `openapi.json`. You can learn more about the [specfication here](https://learn.openapis.org/). 

## Install Docker

**Mac:** install [OrbStack](https://orbstack.dev) (`brew install orbstack`) or
[Docker Desktop](https://www.docker.com/products/docker-desktop/). Either one
provides `docker compose`. Open the app once after installing.

**Windows:** install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
with the WSL 2 backend (OrbStack is Mac-only).

- Step-by-step guides (Dan pulled from web for windows - no idea if these work):
  - [Install Docker Desktop on Windows](https://docs.docker.com/desktop/setup/install/windows-install/) (Docker)
  - [Docker Desktop and WSL 2](https://docs.docker.com/desktop/features/wsl/) (Docker)
  - [WSL best practices](https://docs.docker.com/desktop/features/wsl/best-practices/) (Docker; why to keep code inside WSL)
  - [Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install) (Microsoft)

**Check it works:** `docker --version` and `docker compose version`.

## Run

```sh
docker compose up --build
```

Test express app:

```sh
curl -X POST localhost:3000/items -H 'Content-Type: application/json' -d '{"name":"apple"}'
curl localhost:3000/items
```

Test fastapi app:

```sh
curl -X POST localhost:8000/items -H 'Content-Type: application/json' -d '{"name":"apple"}'
curl localhost:8000/items
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

## Make your own micro service

Copy your prefered framework folder into a new one, ie `cp app1 myserviceName`, then update the docker-compose file with your new apis name. 

Next, make sure you chose a new port.

## Development Process

All new code into the repo needs to be through pull requests. For your service, you should assign the PR to one of you co-devs on the project.

If you change the endpoints, you should also change the spec. We'll create a CD script on github for the PR to check the spec. 

On succesful merge, we should tag MAJOR.MINOR.BUG so we can pin the app-pool code base for our own apps.

#### Microservices & Developers

- Image Microservice: Dan, Russell
- Username Generator: Jacob, Christina, Dan
- CSV Exporter: Russell, Jacob


#### Project Docs

- [Microservices brainstorm doc](https://docs.google.com/document/d/17B7_j38awmuUUlzKKpJpwiFDM6LCf7nKW2YM442B-FE/edit?tab=t.0)
- [Team Diagram](https://oregonstateuniversity-my.sharepoint.com/:p:/r/personal/meltonda_oregonstate_edu/Documents/PNW%20Monoliths%20Team%20Diagram.pptx?d=wbe830cab282745c9bc4f3302ad994861&csf=1&web=1&e=avE2ZP)
