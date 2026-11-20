"""Write HTML, render PDF through Chrome, package EPUB."""
import html
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

from .config import CACHE, CHROME
from .layouts import A4_CSS, BASE_CSS


def write_html(path, css, sections, alt_odd_even=False):
    secs = []
    for i, s in enumerate(sections, 1):
        if alt_odd_even:
            s = s.replace('class="page ', f'class="page {"odd" if i % 2 else "even"} ', 1)
        secs.append(s)
    path.write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>book</title>'
        f"<style>{BASE_CSS}{css}</style></head><body>" + "\n".join(secs) + "</body></html>",
        encoding="utf-8")


def to_pdf(html_path, pdf_path):
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
         "--run-all-compositor-stages-before-draw", f"--print-to-pdf={pdf_path}", html_path.as_uri()],
        check=True, capture_output=True, timeout=180)


def count_pdf_pages(pdf):
    return len(re.findall(rb"/Type\s*/Page[^s]", Path(pdf).read_bytes()))


def build_epub(title, author, slug, sections, image_files, out_path):
    w, h = 794, 1123
    tmp = CACHE / f"epub-{slug}"
    if tmp.exists():
        shutil.rmtree(tmp)
    (tmp / "OEBPS" / "images").mkdir(parents=True)
    (tmp / "META-INF").mkdir()
    (tmp / "mimetype").write_text("application/epub+zip")
    (tmp / "META-INF" / "container.xml").write_text(
        '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
        '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
    css = BASE_CSS + A4_CSS.replace("@page { size: 210mm 297mm; margin: 0; }", "") + f"\nhtml,body{{width:{w}px;height:{h}px;}}"
    (tmp / "OEBPS" / "style.css").write_text(css)
    names = set()
    for src in image_files:
        shutil.copy(src, tmp / "OEBPS" / "images" / Path(src).name)
        names.add(Path(src).name)
    items, spine = [], []
    for i, s in enumerate(sections, 1):
        body = re.sub(r'src="[^"]*?/([^/"]+)"', r'src="images/\1"', s).replace("<br>", "<br/>")
        body = re.sub(r'(<img [^>]*?)(?<!/)>', r"\1/>", body)
        (tmp / "OEBPS" / f"p{i:02d}.xhtml").write_text(
            '<?xml version="1.0" encoding="utf-8"?><!DOCTYPE html>'
            '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"><head>'
            f'<meta charset="utf-8"/><meta name="viewport" content="width={w}, height={h}"/>'
            f'<title>{html.escape(title)} {i}</title><link rel="stylesheet" href="style.css"/></head><body>{body}</body></html>',
            encoding="utf-8")
        items.append(f'<item id="p{i:02d}" href="p{i:02d}.xhtml" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="p{i:02d}"/>')
    img_items = []
    for j, name in enumerate(sorted(names)):
        mt = "image/png" if name.endswith("png") else "image/webp" if name.endswith("webp") else "image/jpeg"
        props = ' properties="cover-image"' if name.startswith("cover") else ""
        img_items.append(f'<item id="img{j}" href="images/{name}" media-type="{mt}"{props}/>')
    (tmp / "OEBPS" / "nav.xhtml").write_text(
        '<?xml version="1.0" encoding="utf-8"?><!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml" '
        'xmlns:epub="http://www.idpf.org/2007/ops"><head><meta charset="utf-8"/><title>Contents</title></head><body>'
        f'<nav epub:type="toc"><ol><li><a href="p01.xhtml">{html.escape(title)}</a></li></ol></nav></body></html>')
    (tmp / "OEBPS" / "content.opf").write_text(
        '<?xml version="1.0" encoding="utf-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bid">'
        f'<metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="bid">urn:ebook-studio:{slug}</dc:identifier>'
        f'<dc:title>{html.escape(title)}</dc:title><dc:creator>{html.escape(author)}</dc:creator><dc:language>en</dc:language>'
        '<meta property="dcterms:modified">2026-01-01T00:00:00Z</meta>'
        '<meta property="rendition:layout">pre-paginated</meta><meta property="rendition:orientation">portrait</meta>'
        '<meta property="rendition:spread">none</meta></metadata><manifest>'
        '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>'
        '<item id="css" href="style.css" media-type="text/css"/>'
        + "".join(items) + "".join(img_items) + "</manifest><spine>" + "".join(spine) + "</spine></package>")
    out_path.unlink(missing_ok=True)
    with zipfile.ZipFile(out_path, "w") as z:
        z.write(tmp / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
        for f in sorted(tmp.rglob("*")):
            if f.is_file() and f.name != "mimetype":
                z.write(f, f.relative_to(tmp).as_posix(), compress_type=zipfile.ZIP_DEFLATED)
