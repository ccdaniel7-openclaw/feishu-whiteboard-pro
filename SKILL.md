---
name: feishu-whiteboard-pro
description: >
  Build polished, EDITABLE Feishu / Lark (飞书) whiteboards from a layout-component library —
  swimlanes, comparison grids, pipelines, system maps, timelines, card grids — via a Python
  generator that auto-wraps text and sizes every container so nothing clips. Use whenever the user
  wants a Feishu/Lark whiteboard, board, 画板, infographic, product map, architecture diagram,
  roadmap, comparison, poster, or visual explainer — especially when it should look like a finished
  artifact, or when a previous board "looked 不好看 / too sparse". Trigger even if they just say "draw
  this on a 飞书画板", "turn this into a board", or "make a 脉络图 / 架构图 / 对比图". Also use it for
  board-backed tasks: visualize a codebase/GitHub repo as one picture, summarize a meeting into a
  长图, turn spreadsheet data into a one-image data viz, explain a paper or blog as interleaved
  boards + text (图文混排, a PPT replacement), or an event poster/海报. Owns the LAYOUT and
  FORMAT (landscape, mobile 长图, or interleaved doc) — what generic board tools leave to chance.
---

# Feishu Whiteboard Pro

A **layout-first** whiteboard skill. Other Feishu-board tools hand you a palette and the
medium's rules, then leave the composition to you — which is exactly where boards go wrong
(sparse, lopsided, text clipping out of boxes). This skill's center of gravity is the
opposite: a **library of finished layout archetypes** with exact coordinate recipes, driven
by a **generator that does the layout arithmetic** (text measurement, chip wrapping,
auto-sizing containers) so the output is clean on the first or second render.

You still compose — but you compose by *choosing an archetype and filling its slots*, not by
inventing pixel coordinates from scratch.

## What makes a board good here
1. **A real layout, not a blob.** Pick an archetype from `references/components.md` that fits
   the content's shape (a flow → pipeline/swimlane; two options → comparison; parts of a
   system → system map; events over time → timeline). The archetype carries the proportions.
2. **Density that fits.** Every region is filled and balanced; no giant empty right half. The
   generator grows containers to their content, so you add information freely without fear of
   overflow.
3. **The medium's limits respected.** Solid fills (no gradients), native arrows, one font,
   type ≥16px. These are hard — see `references/rules.md`. Designs that ignore them render as
   lumpy rasters.

## Prerequisites (check first)
Run `scripts/preflight.sh`. You need: **Node ≥ 20**; **`lark-cli`** (`npm i -g @larksuite/cli`)
installed and authenticated (`lark-cli auth login`); **`@larksuite/whiteboard-cli`** (auto-runs
via `npx`); a Feishu/Lark account (boards write to the user's own tenant). If `lark-cli` isn't
authenticated, walk the user through `lark-cli auth login` (device-flow: show the URL + a QR via
`lark-cli auth qrcode`, wait for them, then complete with `--device-code`).

## Workflow

### 1. Understand the content, then pick a format AND an archetype
First decide the **format**, because it changes every size you'll use:
- **Landscape** (~1680 wide) — the default for product maps, architectures, dashboards viewed on a laptop.
- **Long-image / 长图** (~1080–1200 wide, tall) — for anything consumed on a phone: meeting summaries,
  data viz, posters, codebase explainers. Bigger type floors (body ≥20px). See `references/scenarios.md`.
- **图文混排 doc** — many small boards interleaved with text in one doc; replaces a PPT, explains a
  paper/blog. See `references/scenarios.md`.

If the ask matches a known scenario (codebase viz, meeting summary, data viz, paper/blog explainer,
poster), `references/scenarios.md` maps it straight to a format + archetype. Then open
`references/components.md` and choose the archetype whose *shape* matches the content. Tell the user the
format + archetype + why, in a line. Pick a palette from `references/palettes.md` (cool/blue for systems
& compliance, warm for product/marketing, mono for editorial) and say which.

### 2. Build with the generator
The generator library is `scripts/board.py`. **Import it, don't reinvent it** — it already
solves text measurement and wrapping, which is where hand-written SVG breaks. Pattern:

```python
import sys; sys.path.insert(0, "scripts")
from board import Board
b = Board(width=1680)                       # logical canvas; height auto-fits
# ... call b.rect / b.text / b.chips / b.card / b.arrow / b.node per the archetype recipe ...
b.save("/tmp/diagram.svg")                  # writes board-legal SVG (marker defs + bg)
```

`references/components.md` gives a runnable recipe per archetype. `examples/product_map.py` is a
full worked board (a 3-lane product map) you can read or adapt. Key generator features you
should lean on:
- `b.chips(x, y, items, max_w, ...)` — auto-wrapping pill flow; `items` may be `(label, is_key)`
  tuples to highlight key ones. Returns the bottom y.
- `b.chips_height(items, max_w, ...)` — pre-compute height so you can size a card/lane to fit
  **before** drawing it. This is how you avoid overflow: measure, then draw the container, then
  draw the chips.
- `b.arrow(...)` / `b.polyline(pts)` — native connectors with built-in arrowheads. Never draw a
  triangle as an arrowhead (it rasterizes).
- `b.node(cx, cy, label="↓")` — ringed connector hub between stages.

### 3. Render → look → fix (do not skip)
```bash
scripts/render_check.sh /tmp/diagram.svg     # renders PNG + runs geometric --check
```
Then **actually open the PNG and look.** Fix the usual suspects: text overflowing a box, a
single chip wider than its column, content flush to the canvas edge, accidental overlaps,
anything clipped on the right/bottom. The `--check` pass reports `text-overflow` / `node-overlap`
with pixel amounts — treat overflow errors as must-fix; judge overlaps with your eyes (a
highlighted box sitting flush beside its neighbor is fine). Iterate until clean.

### 4. Write it into Feishu and verify the live board
```bash
# create a doc with an empty whiteboard block; grab block_token from the JSON
lark-cli docs +create --api-version v2 \
  --content '<title>My board</title><whiteboard type="blank"></whiteboard>' --as user
# push the SVG as native, editable shapes
npx -y @larksuite/whiteboard-cli@^0.2.11 -i /tmp/diagram.svg --to openapi --format json \
  | lark-cli whiteboard +update --whiteboard-token <BLOCK_TOKEN> --source - \
      --input_format raw --idempotent-token <unique> --overwrite --as user
# pull the LIVE board image and look (text color is faithful here, unlike the local PNG)
lark-cli whiteboard +query --whiteboard-token <BLOCK_TOKEN> --output_as image --output ./live --as user
```
Deliver **both** the doc link and the rendered image. Note the board is fully editable in Feishu.

## Honest scope
This medium cannot do gradients, soft shadows, translucency, or fine sub-16px type — that's a
hard ceiling (`references/rules.md`), not a missing feature. If a user wants gradient/glass
polish, that only exists as a static image (e.g. HTML→PNG), which is **not** editable. This skill
maximizes beauty *within* the editable-board envelope: strong layout, balanced density, clean
flat color. Set that expectation rather than promising a look the board can't hold.

## Files
- `references/components.md` — **the layout library.** Archetypes + coordinate recipes. Read this to compose.
- `references/scenarios.md` — **scenario → format + archetype map**, plus how to build long-images (长图),
  图文混排 docs (interleaved boards + text), and how to handle photos/images. Read when the ask is a
  real task (codebase viz, meeting summary, data viz, paper/blog, poster) rather than a bare diagram.
- `references/rules.md` — the medium's hard limits and the build/verify commands. Read before building.
- `references/palettes.md` — curated solid palettes (flattened for the medium).
- `scripts/board.py` — the generator library. Import it.
- `scripts/render_check.sh` — render + geometric check in one call.
- `scripts/preflight.sh` — dependency + auth check.
- `examples/product_map.py` — a full worked board using the library.

## Credit
The medium rules and palette philosophy build on the open `beautiful-feishu-whiteboard` skill by
zarazhangrui; this skill adds the missing **layout-component** layer and a generator that
automates the layout math.
