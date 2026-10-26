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

Or with Docker: `docker build -t app1 . && docker run -p 3000:3000 app1`.
