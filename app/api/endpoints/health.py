from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": "metasnap-og-api",
        "version": "1.0.0",
        "engine": "Pillow Dynamic Renderer v12"
    }
