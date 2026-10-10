from pydantic import BaseModel, Field
from typing import Optional

class OGCardRequest(BaseModel):
    title: str = Field(..., examples=["Scale Your SaaS to $10k MRR"], max_length=120)
    subtitle: Optional[str] = Field(None, examples=["Automated workflows and modern tech stack for indie developers."], max_length=240)
    brand_name: Optional[str] = Field("MetaSnap Pro", examples=["MyBrand"], max_length=40)
    domain: Optional[str] = Field("metasnap.io", examples=["mybrand.com"], max_length=60)
    author: Optional[str] = Field("Dev Team", examples=["Alex Rivera"], max_length=40)
    handle: Optional[str] = Field("@founder", examples=["@alex_dev"], max_length=30)
    badge: Optional[str] = Field("FEATURED", examples=["NEW RELEASE"], max_length=25)
    theme: Optional[str] = Field("nebula", examples=["nebula"], description="nebula, cyber, emerald, sunset, or minimal")

class OGCardResponse(BaseModel):
    success: bool
    title: str
    preview_url: str
    dimensions: str = "1200x630"
    format: str = "image/png"
