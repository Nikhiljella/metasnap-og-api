import os

class Settings:
    PROJECT_NAME: str = "MetaSnap Pro Dynamic OG Engine"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Tier rate limits (SlowAPI strings)
    FREE_TIER_RATE_LIMIT: str = "30/minute"
    PRO_TIER_RATE_LIMIT: str = "600/minute"
    
    # Pre-shared Demo API Key for Pro users (Can be extended with Stripe/DB)
    PRO_API_KEYS: set = {"demo-pro-key-2026", "metasnap-vip-unlimited"}
    
    ALLOWED_ORIGINS: list = [
        "http://localhost:5173",
        "http://localhost:3000",
        "https://metasnap.io",
        "*"
    ]

settings = Settings()
