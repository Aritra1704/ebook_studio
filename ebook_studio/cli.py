"""Command line: build or check a story.

  ./build twin-sisters 01          build story 01
  ./build twin-sisters all         build every story in the series
  ./build twin-sisters 01 --check  report what is missing, build nothing
"""
import argparse
import copy

from . import config
from .layouts import A4_CSS, PRINT_CSS
from .outputs import build_epub, count_pdf_pages, to_pdf, write_html
from .pages import Ctx, build_pages
from .text import parse_extras, parse_story
from .images import find_image


def load(story_dir, series_dir, meta):
    title, pages = parse_story(story_dir / "story.md")
    pages = [p for p in pages if p["kind"] != "back"] + parse_extras(story_dir / "extras.md") + [p for p in pages if p["kind"] == "back"]
    # order: intro, story pages, moral, extras, back
    order = {"intro": 0, "story": 1, "moral": 2, "extra": 3, "back": 4}
    pages.sort(key=lambda p: order[p["kind"]])
    wm = series_dir / "assets" / "watermark.png"
    cover = next((c for c in (story_dir / "cover.png", story_dir / "cover.jpg") if c.exists()), None)
    ctx = Ctx(story_dir=story_dir, meta=meta, title=title,
              watermark=wm.as_uri() if wm.exists() else "", cover=cover.as_uri() if cover else "")
    return title, pages, ctx, wm, cover


def sections_for(ctx, pages):
    a4 = build_pages(ctx, pages, front=True)
    pr = build_pages(ctx, copy.deepcopy(pages), front=False, check_images=False)
    if len(pr) % 2:
        pr.append('<section class="page"></section>')
    return a4, pr


def notes(ctx, wm, cover, print_pages, min_pages):
    out = list(ctx.warnings)
    if not wm.exists():
        out.append("series assets/watermark.png missing: building without the banyan watermark")
    if not cover:
        out.append("cover.png missing in the story folder: using a plain title cover")
    if print_pages < min_pages:
        out.append(f"KDP paperback needs at least {min_pages} pages; the print interior has {print_pages}. "
                   "Add more pages (colouring pages, extras.md) before uploading.")
    return out


def check(story_dir, series_dir, meta):
    title, pages, ctx, wm, cover = load(story_dir, series_dir, meta)
    print(f"{story_dir.name}: '{title}'")
    story_pages = [p for p in pages if p["kind"] == "story"]
    missing = [p["head"].split()[1] for p in story_pages if find_image(story_dir, f"p{int(p['head'].split()[1]):02d}")[1]]
    print(f"  pictures: {len(story_pages) - len(missing)}/{len(story_pages)} found" + (f" (missing p{', p'.join(missing)})" if missing else ""))
    a4, pr = sections_for(ctx, pages)
    print(f"  pages: A4/EPUB {len(a4)}, KDP print {len(pr)} (min {meta['kdp']['min_pages']})")
    for n in notes(ctx, wm, cover, len(pr), meta["kdp"]["min_pages"]):
        print("  NOTE:", n)


def build(story_dir, series_dir, meta):
    title, pages, ctx, wm, cover = load(story_dir, series_dir, meta)
    slug = story_dir.name
    dist = story_dir / "dist"
    dist.mkdir(exist_ok=True)
    html_dir = config.CACHE / "html"
    html_dir.mkdir(parents=True, exist_ok=True)
    a4, pr = sections_for(ctx, pages)
    print(f"Building {slug}: '{title}'")
    write_html(html_dir / f"{slug}-a4.html", A4_CSS, a4)
    write_html(html_dir / f"{slug}-kdp-print.html", PRINT_CSS, pr, alt_odd_even=True)
    for kind in ("a4", "kdp-print"):
        pdf = dist / f"{slug}-{kind}.pdf"
        to_pdf(html_dir / f"{slug}-{kind}.html", pdf)
        print(f"  {pdf.name}  {count_pdf_pages(pdf)} pages")
    imgs = [find_image(story_dir, f"p{int(p['head'].split()[1]):02d}")[0] for p in pages if p["kind"] == "story"]
    for extra in (wm if wm.exists() else None, cover):
        if extra:
            imgs.append(extra)
    for p in pages:
        if p["kind"] == "extra":
            from .text import slugify
            for ext in ("png", "jpg", "jpeg"):
                f = story_dir / "extras" / f"{slugify(p['head'])}.{ext}"
                if f.exists():
                    imgs.append(f)
    epub = dist / f"{slug}.epub"
    build_epub(title, meta["author"], slug, a4, imgs, epub)
    print(f"  {epub.name}")
    for n in notes(ctx, wm, cover, len(pr), meta["kdp"]["min_pages"]):
        print("  NOTE:", n)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="build", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("series", help="series folder name, e.g. twin-sisters")
    ap.add_argument("story", help="story number prefix (e.g. 01) or 'all'")
    ap.add_argument("--check", action="store_true", help="only report what is missing")
    a = ap.parse_args(argv)
    try:
        series_dir, meta = config.load_series(a.series)
        for story_dir in config.find_stories(series_dir, a.story):
            (check if a.check else build)(story_dir, series_dir, meta)
    except config.ConfigError as e:
        print(f"error: {e}")
        return 1
    return 0
