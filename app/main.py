from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.api.endpoints import health, og

limiter = Limiter(key_func=get_remote_address, default_limits=[settings.FREE_TIER_RATE_LIMIT])

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
# 🚀 MetaSnap Pro Dynamic OG Image Microservice

High-throughput, distributed image generation microservice engineered for developers, indie hackers, and SaaS platforms.

### Core Capabilities:
- **Instant Edge Generation**: Generates 1200x630px OpenGraph cards in <40ms.
- **Dynamic URL Queries**: Drop directly into `<meta property="og:image" content="...">`.
- **Tiered Rate Limiting**: Built-in protection and monetization tier support.
- **5 Designer Themes**: Nebula, Cyberpunk, Emerald, Solar Sunset, and Sleek Dark.
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Attach SlowAPI limiter state and error handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(health.router)
app.include_router(og.router, prefix=f"{settings.API_V1_PREFIX}/og", tags=["OpenGraph Generation"])

@app.get("/", tags=["System"])
def root():
    return {
        "service": settings.PROJECT_NAME,
        "docs": "/docs",
        "health": "/health",
        "demo_endpoint": "/api/v1/og/generate?title=Hello+World&theme=nebula"
    }
