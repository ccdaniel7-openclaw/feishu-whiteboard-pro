# Feishu Whiteboard — Medium Hard Limits

These are the **non-negotiable** properties of the Feishu SVG board, verified empirically on the
real product. A design that violates them doesn't error — it silently degrades (the offending node
flattens to a lumpy raster image, or a style is ignored), which looks worse than a plain board.
`scripts/board.py` already stays inside these limits; this file is here so you understand *why* the
generator refuses certain things, and so you don't hand-add them.

*(Adapted from the `beautiful-feishu-whiteboard` skill's RULES.md by zarazhangrui — credit to the
original empirical work.)*

## The limits

- **One font.** The board hardcodes Noto Sans SC. Never set `font-family`. Differentiate type by
  **size / weight / casing / letter-spacing** only.
- **Native shapes only.** `<rect>` (sharp or rounded `rx`), `<circle>`, `<ellipse>`, straight
  `<line>` / `<polyline>` connectors, `<text>`. These become real editable shapes. **`<polygon>`
  and any curved/bezier `<path>` embed as flat images** — at most one tiny triangle/diamond as a
  rare accent, never structural. No organic/illustrative shapes (blobs, leaves, waves, stars,
  doodles). If a reference is organic, keep only its palette and rebuild with rects + circles.
- **Arrows = native connectors.** Put a `marker-end` on a `<line>`/`<polyline>` pointing at one
  `<marker>` in `<defs>`; the board renders a clean built-in arrowhead in the line's color.
  **Never draw an arrowhead as a separate triangle** — it rasterizes and looks hand-drawn. (The
  generator's `b.arrow()` / `b.polyline()` do this correctly.)
- **No gradients, filters, patterns, clipPath, masks, blur.** All forbidden — they flatten the
  node to a static image. Depth comes from flat color blocks, role-swaps, scale, and (if needed)
  hard offset shadows (a solid duplicate of the same shape offset behind it — never a blur).
- **Opacity is ignored.** `opacity` / `fill-opacity` / `stroke-opacity` all render fully opaque.
  For a paler tint use a **solid lighter hex**. To fake a translucent overlay, paint the overlap
  region as its own solid shape.
- **Type ≥ ~16px, load-bearing.** Small text on a colored canvas is unreliable in export and hard
  to read. Keep small labels inside high-contrast panels. No decorative micro-chrome
  (kickers/slugs/metadata).
- **Text color:** unrestricted on the live board, but the **local PNG export renders text color
  unreliably (often black).** Judge color on the live board (`--output_as image` after pushing) or
  via stored hex — not the local render.
- **No SVG `<image>`.** Verified: an `<image href=…>` renders **blank** on the board — remote URL
  and base64 data-URI alike, in both the local PNG and the live board. To place a real photo/logo,
  upload it as a media node via `lark-cli docs +media-upload` / `+media-insert` and let the doc
  resolve it server-side; don't embed it in the SVG. See `references/scenarios.md` → "Images".
- **Transforms:** `translate` / `rotate` / `scale` are safe; avoid `skew` / `matrix`.
- **No fixed canvas.** Work in a logical space (~1600–1700 wide) and let content set the height.
- **Text reflows by character** (CJK ≈ 1em, Latin ≈ 0.58em) — which is exactly why `board.py`
  measures every string. Pad boxes; never fit text to the pixel.
- **Never echo the prompt or your process onto the board.** No "summary of… / 来源… / 风格…" lines,
  no scope notes, no file paths, no chosen-template name. A title may name the *subject*; nothing may
  describe the *task*. Put that context in chat, not on the canvas.

## Build / verify commands
```bash
# render to PNG + geometric check (wrapper does both):
scripts/render_check.sh /tmp/diagram.svg
# equivalently:
npx -y @larksuite/whiteboard-cli@^0.2.11 -i /tmp/diagram.svg -o /tmp/diagram.png -f svg
npx -y @larksuite/whiteboard-cli@^0.2.11 -i /tmp/diagram.svg -f svg --check

# push as an editable board, then pull the live image to verify:
lark-cli docs +create --api-version v2 \
  --content '<title>My board</title><whiteboard type="blank"></whiteboard>' --as user
npx -y @larksuite/whiteboard-cli@^0.2.11 -i /tmp/diagram.svg --to openapi --format json \
  | lark-cli whiteboard +update --whiteboard-token <TOK> --source - \
      --input_format raw --idempotent-token <unique> --overwrite --as user
lark-cli whiteboard +query --whiteboard-token <TOK> --output_as image --output ./live --as user
```
`--check` flags `text-overflow` and `node-overlap` with pixel amounts. Overflow errors are
must-fix. Overlap warnings: judge with your eyes (a highlighted box flush beside its neighbor is
intentional and fine).
