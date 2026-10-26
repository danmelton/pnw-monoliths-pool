---
title: app1 (Express)
description: A tiny TypeScript and Express CRUD API for in-memory items.
---

# app1

TypeScript + Express. In-memory `items` CRUD; spec in `openapi.json`.
Node 24 runs `src/index.ts` directly, with no build step.

Run alone:

```sh
npm install
npm start            # http://localhost:3000
npm run typecheck
```

Under `docker compose up` (from the repo root), `src/` is mounted and edits reload live.

To add a package, run `npm install <pkg>` here (it updates `package.json` and
`package-lock.json`), then rebuild: `docker compose up --build -d app1`. The image
runs `npm ci`, which fails if the lockfile doesn't match `package.json`, so don't
edit `package.json` by hand without running `npm install`.

Or with Docker: `docker build -t app1 . && docker run -p 3000:3000 app1`.
