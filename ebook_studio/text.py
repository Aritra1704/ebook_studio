"""Markdown story parsing and small text helpers."""
import html
import re


def parse_story(path):
    chunks = re.split(r"\n---\n", path.read_text(encoding="utf-8"))
    title = re.search(r"^# (.+)$", chunks[0], re.M).group(1).strip()
    pages = []
    for chunk in chunks[1:]:
        chunk = chunk.strip()
        m = re.match(r"\*\*(.+?)\*\*\s*\n(.*)$", chunk, re.S)
        if not m:
            continue
        head, body = m.group(1).strip(), m.group(2).strip()
        body = re.sub(r"\n*\*\*The End\*\*\s*$", "", body).strip()
        low = head.lower()
        if re.fullmatch(r"Page \d+", head):
            kind = "story"
        elif low.startswith("intro"):
            kind = "intro"
        elif low.startswith("moral"):
            kind = "moral"
        elif low.startswith("back"):
            kind = "back"
        else:
            continue
        pages.append({"kind": kind, "head": head, "blocks": parse_blocks(body)})
    return title, pages


def parse_extras(path):
    """extras.md: pages separated by ---, each starting with a **Title** line."""
    if not path.exists():
        return []
    pages = []
    for chunk in re.split(r"\n---\n", path.read_text(encoding="utf-8")):
        m = re.match(r"\s*\*\*(.+?)\*\*\s*\n(.*)$", chunk.strip(), re.S)
        if m:
            pages.append({"kind": "extra", "head": m.group(1).strip(), "blocks": parse_blocks(m.group(2).strip())})
    return pages


def parse_blocks(body):
    blocks = []
    for raw in re.split(r"\n\s*\n", body):
        lines = [l.strip() for l in raw.strip().splitlines() if l.strip()]
        if not lines:
            continue
        if lines == ["{{frame}}"]:
            blocks.append({"frame": True, "verse": False, "lines": []})
            continue
        verse = len(lines) > 1 and max(len(l) for l in lines) < 70
        blocks.append({"frame": False, "verse": verse, "lines": lines if verse else [" ".join(lines)]})
    return blocks


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def inline(text):
    t = html.escape(text, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
    return smart_quotes(t)


def smart_quotes(t):
    out, last, intag = [], " ", False
    for ch in t:
        if ch == "<":
            intag = True
        if intag:
            out.append(ch)
            if ch == ">":
                intag = False
            continue
        if ch == '"':
            ch = "“" if last in " \n([—" else "”"
        elif ch == "'":
            ch = "’"
        out.append(ch)
        last = ch
    return "".join(out)


def blocks_html(blocks):
    parts = []
    for b in blocks:
        if b["frame"]:
            parts.append('<div class="frame"></div>')
        elif b["verse"]:
            parts.append('<p class="verse">' + "<br>".join(inline(l) for l in b["lines"]) + "</p>")
        else:
            parts.append("<p>" + inline(b["lines"][0]) + "</p>")
    return "\n".join(parts)
