# ebook-studio

Builds picture-book ebooks from markdown text plus page images:

| Output | Use |
|---|---|
| `<story>-a4.pdf` | Direct sale / sharing (A4 portrait, with cover) |
| `<story>-kdp-print.pdf` | Amazon KDP paperback interior, 8.5 x 8.5 in + 0.125 in bleed |
| `<story>.epub` | Kindle, fixed-layout |

The code lives here. The books (text, pictures, outputs) live in a separate **library** on the external drive, so this
project stays small and stays out of iCloud.

## Setup (once)

```bash
pip3 install -r requirements.txt
```

Needs Google Chrome (used to print the PDFs) and the external drive plugged in.
The library path is in `config.toml` (`/Volumes/Ari_HDD_01/stories`); override with `EBOOK_LIBRARY=/other/path`.

## Use

```bash
./build twin-sisters 01
```

```bash
./build twin-sisters 01 --check
```

```bash
./build twin-sisters all
```

`--check` reports missing pictures, watermark, cover and page counts without building. Outputs are written to
`<story folder>/dist/`.

## Library layout

```
/Volumes/Ari_HDD_01/stories/
  twin-sisters/                  one series
    series.toml                  author, imprint, ages, social handle, KDP minimum pages
    assets/watermark.png         faint banyan, used on every story (optional)
    docs/                        series bible, style guide, upcoming stories
    01-the-torn-letter/          one story
      story.md                   the text (intro, Page 1..N, Moral, Back cover)
      extras.md                  extra pages after the moral (optional)
      images/p01.png ... p11.png page pictures, square, 1200 px or more
      extras/<page-title>.png    optional picture for an extra page, e.g. meet-mira-and-maya.png
      cover.png                  full-page cover (optional)
      dist/                      generated PDFs and EPUB
```

New story: copy a story folder, rename it `02-...`, edit `story.md`, add pictures, build.
New series: copy `twin-sisters` and edit `series.toml`.

## Story file format

Pages are separated by `---`, each starting with a bold header: `**Intro page**`, `**Page 1**` ... `**Moral of the Story**`,
`**Back cover**`. Blocks of short lines (under 70 characters) are laid out as verse. Use `*italic*` and `**bold**`.
In `extras.md`, a line containing only `{{frame}}` draws a dashed drawing box.

## Notes

- Font: Merriweather if installed, otherwise Georgia. The EPUB uses the reader's own serif font (Georgia cannot be embedded).
- KDP: the paperback needs 24+ pages; the cover is a separate full-wrap file sized from the spine width.
- The EPUB has not been run through Amazon's epubcheck.
# ebook_studio
