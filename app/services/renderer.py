import io
import math
from PIL import Image, ImageDraw, ImageFont

# Gradient color schemes matching MetaSnap frontend
THEMES = {
    "nebula": {
        "start": (46, 16, 101),   # Dark Violet
        "mid": (30, 27, 75),      # Indigo 950
        "end": (2, 6, 23),        # Slate 950
        "accent": (129, 140, 248),# Indigo 400
        "text": (255, 255, 255),
        "subtext": (203, 213, 225)
    },
    "cyber": {
        "start": (112, 26, 117),  # Fuchsia 900
        "mid": (59, 7, 100),      # Purple 950
        "end": (2, 6, 23),
        "accent": (232, 121, 249),
        "text": (255, 255, 255),
        "subtext": (226, 232, 240)
    },
    "emerald": {
        "start": (6, 78, 59),     # Emerald 900
        "mid": (4, 47, 46),       # Teal 950
        "end": (2, 6, 23),
        "accent": (52, 211, 153),
        "text": (255, 255, 255),
        "subtext": (209, 250, 229)
    },
    "sunset": {
        "start": (124, 45, 18),   # Orange 900
        "mid": (69, 26, 3),       # Amber 950
        "end": (2, 6, 23),
        "accent": (251, 146, 60),
        "text": (255, 255, 255),
        "subtext": (254, 215, 170)
    },
    "minimal": {
        "start": (30, 41, 59),    # Slate 800
        "mid": (15, 23, 42),      # Slate 900
        "end": (2, 6, 23),
        "accent": (148, 163, 184),
        "text": (255, 255, 255),
        "subtext": (148, 163, 184)
    }
}

def render_og_image(
    title: str,
    subtitle: str = None,
    brand_name: str = "MetaSnap Pro",
    domain: str = "metasnap.io",
    author: str = "Engineering Team",
    handle: str = "@builder",
    badge: str = "VERIFIED",
    theme: str = "nebula",
    watermark: bool = False
) -> bytes:
    """
    Renders a pixel-perfect 1200x630 OpenGraph card into PNG bytes.
    """
    width = 1200
    height = 630

    cfg = THEMES.get(theme.lower(), THEMES["nebula"])
    start_c = cfg["start"]
    mid_c = cfg["mid"]
    end_c = cfg["end"]
    accent_c = cfg["accent"]
    text_c = cfg["text"]
    subtext_c = cfg["subtext"]

    # Generate smooth 2D angular gradient
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)

    for y in range(height):
        # Progress 0.0 -> 1.0
        p = y / float(height)
        if p < 0.5:
            # Interpolate start -> mid
            local_p = p * 2.0
            r = int(start_c[0] * (1 - local_p) + mid_c[0] * local_p)
            g = int(start_c[1] * (1 - local_p) + mid_c[1] * local_p)
            b = int(start_c[2] * (1 - local_p) + mid_c[2] * local_p)
        else:
            # Interpolate mid -> end
            local_p = (p - 0.5) * 2.0
            r = int(mid_c[0] * (1 - local_p) + end_c[0] * local_p)
            g = int(mid_c[1] * (1 - local_p) + end_c[1] * local_p)
            b = int(mid_c[2] * (1 - local_p) + end_c[2] * local_p)
        
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Outer border / frame
    border_color = (accent_c[0], accent_c[1], accent_c[2], 120)
    draw.rounded_rectangle([(30, 30), (width - 30, height - 30)], radius=24, outline=accent_c, width=3)

    # Ambient Accent Glow in bottom-right
    glow_center = (width - 150, height - 150)
    for rad in range(120, 10, -10):
        alpha = int(15 * (1 - rad / 120))
        glow_color = (accent_c[0], accent_c[1], accent_c[2])
        draw.ellipse([
            (glow_center[0] - rad, glow_center[1] - rad),
            (glow_center[0] + rad, glow_center[1] + rad)
        ], outline=glow_color, width=2)

    # Use default / system scalable font
    try:
        font_brand = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
        font_domain = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 20)
        font_badge = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
        font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 54)
        font_subtitle = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 26)
        font_footer = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 22)
    except Exception:
        font_brand = ImageFont.load_default()
        font_domain = ImageFont.load_default()
        font_badge = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_footer = ImageFont.load_default()

    # Draw Brand Header
    draw.rectangle([(70, 70), (114, 114)], fill=accent_c)
    draw.text((82, 76), brand_name[:1].upper(), font=font_brand, fill=(0, 0, 0))
    draw.text((130, 72), brand_name, font=font_brand, fill=text_c)
    draw.text((130, 108), domain, font=font_domain, fill=accent_c)

    # Draw Badge Pill
    badge_text = f" {badge.upper()} "
    draw.rounded_rectangle([(width - 240, 70), (width - 70, 114)], radius=12, fill=(0, 0, 0, 180), outline=accent_c, width=2)
    draw.text((width - 220, 80), badge_text, font=font_badge, fill=accent_c)

    # Draw Wrapped Title
    def wrap_text(text, max_chars=40):
        words = text.split()
        lines = []
        cur = []
        for w in words:
            if sum(len(x) for x in cur) + len(cur) + len(w) <= max_chars:
                cur.append(w)
            else:
                lines.append(" ".join(cur))
                cur = [w]
        if cur:
            lines.append(" ".join(cur))
        return lines

    title_lines = wrap_text(title, max_chars=36)[:3]
    y_text = 200
    for line in title_lines:
        draw.text((70, y_text), line, font=font_title, fill=text_c)
        y_text += 68

    # Draw Subtitle if present
    if subtitle:
        sub_lines = wrap_text(subtitle, max_chars=65)[:2]
        y_text += 10
        for line in sub_lines:
            draw.text((70, y_text), line, font=font_subtitle, fill=subtext_c)
            y_text += 36

    # Horizontal divider
    draw.line([(70, 520), (width - 70, 520)], fill=(255, 255, 255, 40), width=1)

    # Draw Footer Attribution
    draw.ellipse([(70, 545), (106, 581)], fill=accent_c)
    draw.text((82, 548), author[:1].upper(), font=font_brand, fill=(0, 0, 0))
    draw.text((120, 552), f"{author} • {handle}", font=font_footer, fill=text_c)

    if watermark:
        draw.text((width - 280, 552), "⚡ Built with MetaSnap", font=font_footer, fill=(148, 163, 184))
    else:
        draw.text((width - 220, 552), "★ Verified Card", font=font_footer, fill=accent_c)

    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()
