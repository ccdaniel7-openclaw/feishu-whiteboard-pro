# Scenario & Format Playbook

The board's real power isn't one pretty diagram — it's that the output is **editable,
collaborative, and commentable inside Feishu** (unlike an HTML screenshot). That unlocks
formats beyond a single landscape chart. This file maps common asks to a recommended
**archetype + canvas format**, and covers the two formats the base workflow doesn't:
**tall mobile images (长图)** and **interleaved documents (图文混排): boards + text**.

## Scenario → recipe

| The user wants… | Archetype (`components.md`) | Format | Notes |
|---|---|---|---|
| Explain a **codebase / GitHub project** as one picture | System map + pipeline | Long-image | Read the actual code, not just the README. Group by module; wire data/control flow with native connectors. |
| **Meeting summary** (from notes/transcript) | Card grid or swimlane (by topic/decision) | Long-image | Clear, complete, readable. One topic per card; pull decisions & owners out as chips. |
| **Data viz from a spreadsheet** | Card grid (KPIs) + comparison + a bar built from rects | Long-image | Bars/columns are just sized `rect`s — no chart engine. Call out top items and the trend in words. |
| **Explain a paper / tech blog** | Pipeline / system map per section | Interleaved doc | Multiple small boards interleaved with prose; one board per concept. |
| **Replace a PPT / share-out** | One board per "slide" | Interleaved doc | Each board is a slide; weave the transcript text between them so the deck carries the spoken nuance. |
| **Event poster** (speakers, agenda) | Card grid (one tile per person) + title banner | Long-image, mobile | Needs real photos → see "Images" below (NOT SVG `<image>`). |
| **Product map / architecture / roadmap** | Swimlane / system map / timeline | Landscape (default) | The base workflow. |

When you pick, say which archetype + format and why in one line, then build.

## Format A — Tall mobile image (长图) for phones
Most of the scenarios above are consumed on a phone in Feishu, scrolled top-to-bottom. A wide
landscape board forces pinch-zoom and loses people. Build **tall and narrowish** instead.

Guidelines:
- **Width ~1080–1200** (not 1680). Height grows freely — `Board` auto-fits it.
- **Bigger type floors:** body ≥ 20px, labels ≥ 18px, titles 48–64px. On a phone, 16px is the
  practical floor; the base workflow's 16px is for landscape viewed on a laptop.
- **Stack vertically, one idea per band.** Full-width sections down the page (a title block, then
  section after section), not 4 side-by-side columns. Chips wrap within the full width.
- **Section rhythm:** a colored full-width header strip, then its content, then the next. Number
  them so the scroll has a spine.
- Verify by viewing the PNG **scaled down to phone size** — if a label is unreadable thumbnailed,
  it's too small.

Follow the same **measure → size → draw** habit as the rest of the skill: wrap the body text,
size a card to hold it, then draw the card, the header strip, and the text into it. (Drawing free
text below a strip with no container both looks loose and trips the overflow linter.)
```python
from board import Board, wrap
b = Board(width=1120)                                        # tall canvas
inner = b.W - 2*b.P
b.text(b.P, 90, "Meeting Summary", 56, "#1E3A8A", "bold")
y = 160
for i, (head, body) in enumerate(sections):
    lines = wrap(body, inner - 40, 21)                       # measure first
    card_h = 54 + 16 + len(lines)*32 + 12                    # header + body fit
    b.card(b.P, y, inner, card_h, fill="#FFFFFF", rx=12, stroke="#E2E8F0", sw=1)
    b.rect(b.P, y, inner, 54, "#2A4BC4", rx=12)              # header strip (sits on the card)
    b.text(b.P+20, y+35, f"{i+1}. {head}", 24, "#EBF1FF", "bold")
    ty = y + 54 + 32
    for ln in lines:
        b.text(b.P+20, ty, ln, 21, "#334155"); ty += 32
    y += card_h + 22
b.save("/tmp/summary.svg")
```

## Format B — Interleaved document (图文混排): boards + text
A Feishu doc can hold **many whiteboard blocks interleaved with text** — the format that
replaces a PPT (each board = a slide, prose between them carries what you said) or explains a
paper/blog section by section.

Build it in two passes:
1. **Create the doc with all blocks in order.** The `--content` of `docs +create` is mini-HTML;
   put `<p>` text and `<whiteboard type="blank">` blocks in the sequence you want. Capture each
   whiteboard block's `block_token` from the response (they come back in document order).
   ```bash
   lark-cli docs +create --api-version v2 --as user --content \
   '<title>Explaining X</title>
    <h1>Part 1 — the idea</h1><p>Prose that sets up the first board…</p>
    <whiteboard type="blank"></whiteboard>
    <h1>Part 2 — how it flows</h1><p>More prose…</p>
    <whiteboard type="blank"></whiteboard>'
   ```
2. **Fill each board** by token with the usual generate → `--to openapi` → `whiteboard +update`
   loop (one SVG per block). Keep each board small and single-purpose — a concept, not a poster.

To **add text around an existing board** later, use `lark-cli docs +update` (append/insert blocks)
or `docs +media-insert --selection-with-ellipsis` to place relative to a text selection.

## Images (photos, logos, external materials)
**Verified:** SVG `<image href=…>` does **not** render on the board — not from a remote URL, not
from a base64 data-URI, in neither the local PNG nor the live board. Don't reach for `<image>`.

To put a real photo/logo on a board (e.g. speaker headshots on a poster), upload it as a media
node via lark-cli and place it, rather than embedding in the SVG:
- `lark-cli docs +media-upload` / `docs +media-insert` — upload a local image into the doc and
  insert it (the doc/board resolves it server-side and returns a token).
- Compose the board layout in SVG first (title, name/title chips, a placeholder rect where each
  photo goes), then upload+place the photos into those slots.
- Always download photos locally first; pass local files to the upload command (remote URLs are
  not fetched). Verify on the **live** board, since the local PNG never shows uploaded media.

If photos are central and the media flow is blocked, say so and offer a layout with name/role
cards instead of headshots — don't ship blank boxes where images were supposed to be.
