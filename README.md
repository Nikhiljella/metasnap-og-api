# MetaSnap Pro — Dynamic OG Image Generation Microservice

> **High-Performance FastAPI Image Generation Engine**  
> Built autonomously using the **`api-microservice-builder`** agent skill.

---

## ⚡ Overview

A sub-40ms dynamic OpenGraph rendering engine for SaaS platforms, content sites, blogs, and marketing automation.

### Endpoints
- `GET /health` — Microservice healthcheck
- `GET /docs` — Interactive OpenAPI / Swagger UI
- `GET /api/v1/og/generate` — Dynamic image URL generator (drop into `<meta property="og:image">`)
- `POST /api/v1/og/generate` — JSON batch generation endpoint

### Designer Color Themes
- `nebula`: Midnight Dark Indigo/Violet
- `cyber`: Cyberpunk Neon Magenta
- `emerald`: High-tech Matrix Emerald
- `sunset`: Warm Solar Ember
- `minimal`: Clean Slate Dark

---

## 🚀 Quickstart

### 1. Local Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.

### 2. Docker Run
```bash
docker compose up --build -d
```

### 3. Run Automated Tests
```bash
pytest -v
```
