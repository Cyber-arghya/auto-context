---
name: docker-ops
version: 1.0.0
description: Production multi-stage Dockerfile and Compose setup, container diagnostics, cleanup, and logging.
triggers: ["docker", "container", "compose", "dockerfile", "entrypoint"]
---

# Skill: Docker Operations & Container Management

## Overview
Standard operating procedures for containerizing applications, writing secure multi-stage Dockerfiles, managing docker-compose stacks, and diagnosing container failures.

## When to Activate
- When creating or modifying `Dockerfile` or `docker-compose.yml`.
- When diagnosing crashed, restarting, or unhealthy containers.
- When cleaning up dangling images, unused volumes, or container build cache.

## Workflows & Procedures

### 1. Multi-Stage Dockerfile Best Practices
* **Principle:** Keep production images minimal by separating build tools from runtime.
* **Non-Root Execution:** Always create and switch to a non-privileged user (e.g. `USER appuser`).
* **Layer Caching:** Copy dependency manifests (`package.json`, `requirements.txt`, `go.mod`) and install dependencies BEFORE copying the application source code.
* **Example (Node/Python pattern):**
  ```dockerfile
  # Build Stage
  FROM node:20-alpine AS builder
  WORKDIR /app
  COPY package*.json ./
  RUN npm ci
  COPY . .
  RUN npm run build

  # Runner Stage
  FROM node:20-alpine AS runner
  WORKDIR /app
  ENV NODE_ENV=production
  RUN addgroup -S appgroup && adduser -S appuser -G appgroup
  COPY --from=builder /app/package*.json ./
  COPY --from=builder /app/dist ./dist
  RUN npm ci --omit=dev
  USER appuser
  EXPOSE 3000
  CMD ["node", "dist/index.js"]
  ```

### 2. Stack Orchestration (`docker-compose.yml`)
* Keep environment variables decoupled using `.env` referencing (`${VAR_NAME}`).
* Define explicit health checks and resource limits:
  ```yaml
  services:
    web:
      build: .
      ports:
        - "3000:3000"
      env_file: .env
      deploy:
        resources:
          limits:
            cpus: '1.0'
            memory: 512M
      healthcheck:
        test: ["CMD", "wget", "-qO-", "http://localhost:3000/health"]
        interval: 30s
        timeout: 5s
        retries: 3
  ```

### 3. Diagnostics & Troubleshooting Commands
* **Inspect logs:** `docker compose logs -f --tail=100 <service>`
* **Inspect container resource consumption:** `docker stats --no-stream`
* **Shell into container:** `docker exec -it <container_name> /bin/sh`
* **Safe Clean-up (reclaim disk space):**
  ```bash
  # Remove stopped containers and dangling images
  docker system prune -f
  # Remove unused build cache
  docker builder prune -f
  ```
