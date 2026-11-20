"""Page pictures: find them, make placeholders, check print resolution."""
from pathlib import Path

from .config import CACHE


def find_image(story_dir, name):
    """name like 'p01'. Returns (path, is_placeholder)."""
    for ext in ("png", "jpg", "jpeg", "webp"):
        p = story_dir / "images" / f"{name}.{ext}"
        if p.exists():
            return p, False
    return placeholder(story_dir.name, name), True


def placeholder(story, name):
    from PIL import Image, ImageDraw, ImageFont
    out = CACHE / "placeholders" / story
    out.mkdir(parents=True, exist_ok=True)
    p = out / f"{name}.png"
    if not p.exists():
        img = Image.new("RGB", (1500, 1500), (247, 240, 220))
        d = ImageDraw.Draw(img)
        try:
            f = ImageFont.load_default(size=90)
        except TypeError:
            f = ImageFont.load_default()
        d.rectangle([60, 60, 1440, 1440], outline=(200, 185, 150), width=8)
        d.text((750, 750), f"ILLUSTRATION\n{name}", fill=(170, 150, 110), font=f, anchor="mm", align="center")
        img.save(p)
    return p


def pixel_warning(p, min_px=1200):
    from PIL import Image
    with Image.open(p) as im:
        if min(im.size) < min_px:
            return f"{Path(p).name}: {im.size[0]}x{im.size[1]}px is below {min_px}px (300 dpi at 4 in) for print"
    return None
