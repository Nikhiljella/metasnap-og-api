from fastapi import Header, HTTPException, status
from app.core.config import settings
from typing import Optional

def verify_api_tier(x_api_key: Optional[str] = Header(None)) -> dict:
    """
    Validates API key tier. Free tier requests require no key but are strictly throttled.
    Pro API keys unlock unlimited edge generation and watermark removal.
    """
    if not x_api_key:
        return {"tier": "free", "authorized": True}
    
    if x_api_key in settings.PRO_API_KEYS or x_api_key.startswith("ms_live_"):
        return {"tier": "pro", "authorized": True}
        
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid MetaSnap API Key. Upgrade to Pro at https://metasnap.io for credentials."
    )
