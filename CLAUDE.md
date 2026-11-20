# ebook-studio: context for Claude

Aritra is writing and selling children's picture books (ages 7-9) under the imprint "A Said Out Loud". This project
builds the ebooks. The books themselves are NOT in this repo; they live on the external drive.

## Two locations

- **Code (this repo):** `/Users/aritrarpal/dev/workspace_biz/ebook-studio` (outside iCloud on purpose).
- **Library (stories, pictures, outputs):** `/Volumes/Ari_HDD_01/stories` (path set in `config.toml`, override with
  `EBOOK_LIBRARY`). The drive may be unplugged; the builder reports that. Ignore the hidden `._*` files on the drive.

Current series: `/Volumes/Ari_HDD_01/stories/twin-sisters` (Mira & Maya). Read its `docs/series-bible-and-upcoming-stories.md`
and `docs/style-guide.md` before writing or changing any story text.

## What it builds

`./build twin-sisters 01` writes to the story's `dist/`: `*-a4.pdf` (direct sale), `*-kdp-print.pdf` (Amazon paperback
interior, 8.5x8.5 in + bleed), `*.epub` (Kindle fixed-layout). `--check` reports what is missing. PDFs are printed through
headless Google Chrome from generated HTML. Code is in `ebook_studio/` (text, pages, layouts, outputs, cli).

## The series in one paragraph

Twin sisters Mira (quiet, observant) and Maya (curious, talkative), age 7, in a third-floor flat near Gariahat, Kolkata,
with Ma and Dida (maternal grandmother, lives with them). Father not introduced yet. Nine more stories are planned
(see the upcoming-stories table in the bible). Story 1, "The Torn Letter" (honesty), and story 2, "The Tram Seat" (empathy), are written.

## Writing and layout rules (from his two earlier ebooks)

- ~11 story pages: one beat per page, 60-90 words of prose, alternating with 8-line AABB rhyming verse pages
  (last couplet bold), then a "Moral of the Story" page, then extras, then a back-cover blurb.
- Start in the middle of the moment. No long scene-setting or character intros. Short, precise, aimed at the lesson.
- No moralising inside the story; the lesson is stated only on the Moral page.
- Look: watercolour pictures in a rounded square at the top, text below, faint banyan watermark, Merriweather-style serif.

## Status and open items

- Pictures not made yet (`images/p01.png`...`p11.png`, square, 1200px+). He makes them with AI tools; keep Mira and
  Maya's outfits and faces consistent (suggested: Maya pink frock + two ponytails, Mira pale green frock + one plait).
- Missing: `assets/watermark.png` (banyan, extract from his earlier PDFs in Google Drive "Canva Ebook"), a cover per story
  (designed in Canva, saved as `cover.png`), and the paperback is 20 pages but KDP needs 24 (e.g. four colouring pages).
- Font: using Georgia fallback; Merriweather not installed (free, Google Fonts; ask before downloading).
- Check the Instagram handle in `series.toml` (`said0utloud`, zero vs letter O).
- EPUB has not been validated with epubcheck. Git is initialised here, nothing committed yet.
- Next story to write: #3 "Who Gets the Last Rosogolla?" (fairness), then the rest of the table in the bible.
- Each story folder has story.md, extras.md (meet/discussion/draw/coming-next pages) and images/ (empty until pictures exist).

## Working preferences

Wants short, direct answers. Ask before downloading files, publishing, or committing. Do not store anything in iCloud
(`~/Documents`, `~/Desktop`).
