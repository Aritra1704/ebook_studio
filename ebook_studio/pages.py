"""Turn parsed pages into <section> html for one layout."""
import re
from dataclasses import dataclass, field

from .images import find_image, pixel_warning
from .text import blocks_html, inline, slugify


@dataclass
class Ctx:
    story_dir: object
    meta: dict
    title: str
    watermark: str = ""      # file:// uri or ""
    cover: str = ""
    warnings: list = field(default_factory=list)


def _wm(uri, cls):
    return f'<img class="{cls}" src="{uri}" alt="">' if uri else ""


def build_pages(ctx, pages, front=True, check_images=True):
    out = []
    m, wm = ctx.meta, ctx.watermark

    def sec(inner, cls=""):
        out.append(f'<section class="page {cls}">{inner}</section>')

    if front:
        if ctx.cover:
            sec(f'<img class="cover-full" src="{ctx.cover}" alt="Cover">')
        else:
            sec(f'{_wm(wm, "wm-big")}<div class="center mid"><h1 class="title-big">{inline(ctx.title)}</h1></div>')
    sec(
        f'{_wm(wm, "wm-big")}<div class="center mid frontmatter"><h1 class="title-med">{inline(ctx.title)}</h1>'
        f'<p>Written by {m["author"]}<br>Illustrations by {m.get("illustrations", "AI-assisted tools")}</p>'
        f'<p>{m["imprint"]}</p><p>{m["ages"]}</p></div>'
    )
    sec(
        _wm(wm, "wm-big") + f'<div class="center mid legal"><p>© {m["year"]} {m["author"]}</p><p>All rights reserved.</p>'
        "<p>No part of this book may be reproduced, distributed, or transmitted in any form or by any means, "
        "including electronic, mechanical, photocopying, recording, or otherwise, without prior written "
        "permission of the author, except for brief quotations in reviews.</p>"
        "<p>This is a work of fiction. Any resemblance to actual persons, living or dead, or actual events "
        "is purely coincidental.</p>"
        f'<p>Illustrations created using {m.get("illustrations", "AI-assisted tools")}.</p><p>First edition.</p>'
        f'<p>Follow more stories and creations at:<br>{m["social"]}</p></div>'
    )
    last_num = max((int(p["head"].split()[1]) for p in pages if p["kind"] == "story"), default=0)
    for p in pages:
        k = p["kind"]
        if k == "intro":
            sec(f'{_wm(wm, "wm-big")}<div class="center mid frontmatter">{blocks_html(p["blocks"])}</div>')
        elif k == "story":
            n = int(p["head"].split()[1])
            img, is_ph = find_image(ctx.story_dir, f"p{n:02d}")
            if check_images and not is_ph:
                w = pixel_warning(img)
                if w:
                    ctx.warnings.append(w)
            sec(f'<img class="img" src="{img.as_uri()}" alt="Illustration for page {n}">'
                f'<div class="body">{blocks_html(p["blocks"])}</div>{_wm(wm, "wm-small")}<div class="num">{n}</div>')
        elif k == "moral":
            sec(f'<h2 class="moral-head">{inline(p["head"])}</h2><div class="body">{blocks_html(p["blocks"])}</div>'
                f'{_wm(wm, "wm-small")}<div class="num">{last_num + 1}</div>')
        elif k == "extra":
            img = ""
            for ext in ("png", "jpg", "jpeg"):
                f = ctx.story_dir / "extras" / f"{slugify(p['head'])}.{ext}"
                if f.exists():
                    img = f'<img class="img" src="{f.as_uri()}" alt="">'
                    break
            sec(f'{img}<h2 class="moral-head">{inline(p["head"])}</h2><div class="body">{blocks_html(p["blocks"])}</div>'
                f'{_wm(wm, "wm-small")}', "extra")
        elif k == "back":
            bl = p["blocks"]
            hook = inline(re.sub(r"^\*\*|\*\*$", "", bl[0]["lines"][0]))
            sec(f'{_wm(wm, "wm-big")}<div class="center mid"><p class="back-hook">{hook}</p>'
                f'<div class="back-body">{blocks_html(bl[1:])}</div></div>')
    return out
