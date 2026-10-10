from fastapi import APIRouter, Response, Depends, Query, Request
from app.schemas.og_card import OGCardRequest, OGCardResponse
from app.services.renderer import render_og_image
from app.core.security import verify_api_tier
from typing import Optional

router = APIRouter()

@router.get(
    "/generate",
    summary="Dynamic Edge OG Image Endpoint",
    description="Generates a live 1200x630 OpenGraph graphic. Perfect for `<meta property='og:image' content='...'>`.",
    response_class=Response,
    responses={200: {"content": {"image/png": {}}}}
)
def generate_og_image_get(
    request: Request,
    title: str = Query("Build Fast, Scale Effortlessly", description="Main headline of the card"),
    subtitle: Optional[str] = Query(None, description="Subtitle or description text"),
    brand_name: Optional[str] = Query("MetaSnap Pro", description="Your brand name"),
    domain: Optional[str] = Query("metasnap.io", description="Domain name"),
    author: Optional[str] = Query("Engineering Team", description="Author name"),
    handle: Optional[str] = Query("@builder", description="Social media handle"),
    badge: Optional[str] = Query("NEW RELEASE", description="Tag badge"),
    theme: Optional[str] = Query("nebula", description="nebula, cyber, emerald, sunset, or minimal"),
    tier_info: dict = Depends(verify_api_tier)
):
    watermark = (tier_info.get("tier") == "free")
    
    png_bytes = render_og_image(
        title=title,
        subtitle=subtitle,
        brand_name=brand_name,
        domain=domain,
        author=author,
        handle=handle,
        badge=badge,
        theme=theme,
        watermark=watermark
    )
    
    return Response(
        content=png_bytes,
        media_type="image/png",
        headers={
            "Cache-Control": "public, max-age=86400, s-maxage=86400",
            "X-MetaSnap-Tier": tier_info.get("tier", "free")
        }
    )

@router.post(
    "/generate",
    summary="JSON Payload OG Image Generator",
    description="Accepts structured JSON payloads for batch generation and enterprise pipelines.",
    response_class=Response,
    responses={200: {"content": {"image/png": {}}}}
)
def generate_og_image_post(
    payload: OGCardRequest,
    tier_info: dict = Depends(verify_api_tier)
):
    watermark = (tier_info.get("tier") == "free")
    
    png_bytes = render_og_image(
        title=payload.title,
        subtitle=payload.subtitle,
        brand_name=payload.brand_name,
        domain=payload.domain,
        author=payload.author,
        handle=payload.handle,
        badge=payload.badge,
        theme=payload.theme,
        watermark=watermark
    )
    
    return Response(
        content=png_bytes,
        media_type="image/png",
        headers={
            "Cache-Control": "public, max-age=86400, s-maxage=86400",
            "X-MetaSnap-Tier": tier_info.get("tier", "free")
        }
    )
