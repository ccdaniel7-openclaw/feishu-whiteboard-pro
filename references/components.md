# Layout Component Library

This is the part generic board tools leave to chance. Each archetype below is a **finished
composition** with proportions that read well, plus a runnable recipe built on `scripts/board.py`.
Pick the one whose shape matches your content, fill its slots, render, fix.

All recipes assume:
```python
import sys; sys.path.insert(0, "scripts")
from board import Board, text_w, wrap
b = Board(width=1680)
```

## Choosing an archetype
| Content shape | Archetype | Why |
|---|---|---|
| A process / value chain with stages | **Swimlane** or **Pipeline** | makes the left→right (or top→down) progression the hero |
| Two or more options weighed | **Comparison grid** | parallel columns force like-for-like rows |
| Parts of one system + how they relate | **System map** | boxes + native connectors show topology |
| Events / milestones over time | **Timeline** | a spine with dated nodes |
| A flat set of peer items | **Card grid** | even tiles, no false hierarchy |
| One layer that underpins all others | **Base dock** (add-on) | a full-width band beneath the main composition |

You can compose add-ons (a context bar on top, a base dock at the bottom, a throughline pill)
onto any archetype — see the end of this file.

---

## 1. Swimlane (stacked) — best for a staged chain with rich per-stage detail
Each stage is a full-width lane: a colored **header rail** on the left (name, role, one-line
positioning, owners) and a white **detail area** on the right (several labeled columns of chips
plus a highlighted "goal" column). Stages connect via a ringed node + arrow down the left rail.
This is the densest archetype — it holds the most information without feeling cramped, because
each lane is its own balanced mini-layout. *(See `examples/product_map.py` for a full worked board.)*

Recipe (one lane; loop over your stages):
```python
P, W = b.P, b.W
laneL_w = 300
laneR_x = P + laneL_w
laneR_w = W - P - laneR_x
padx, pady, gap = 28, 22, 22
col_w = (laneR_w - 2*padx - 3*gap) / 4        # 3 content cols + 1 goal col

cols = [("Channels", ["Web","Email","API"]),
        ("Capabilities", ["Login","Multi-language","Request Form","Attachments"]),
        ("Key Needs", [("Submission UX", True), ("Notifications", False)])]
goal = ["Higher request quality","Fewer follow-up loops"]

# size the lane to the TALLER of its two sides BEFORE drawing (this prevents overflow):
content_h = max([28 + b.chips_height(items, col_w) for _, items in cols]
                + [28 + len(goal)*30])
lane_h = max(pady*2 + content_h + 60, 200)
y = 300                                         # top of this lane

b.card(P, y, laneL_w, lane_h, fill="#2A4BC4")               # left rail (lane color)
b.text(P+26, y+32, "STAGE 01 · INTAKE", 13, "#EBF1FF", "bold")
b.text(P+26, y+70, "Portal", 32, "#EBF1FF", "bold")
b.text(P+26, y+92, "Capture Better", 17, "#EBF1FF", "bold")
# one-line positioning inside a solid lighter block (fake translucency — opacity is ignored):
for i, ln in enumerate(wrap("Unified entry for inbound requests", laneL_w-60, 15)):
    b.text(P+36, y+128+i*22, ln, 15, "#EBF1FF")

b.card(laneR_x, y, laneR_w, lane_h, fill="#FFFFFF")          # detail area
cx = laneR_x + padx
for i, (h4, items) in enumerate(cols):
    x = cx + i*(col_w+gap)
    b.text(x, y+pady+12, h4, 15, "#94A3B8", "bold", ls="0.5", upper=True)
    b.chips(x, y+pady+28, items, col_w,
            key_fill="#DCE5FF", key_stroke="#1E3A8A", key_tx="#1E3A8A")
gx = cx + 3*(col_w+gap)                                      # highlighted goal column
goal_h = 28 + len(goal)*30
b.rect(gx-12, y+pady-6, col_w+18, goal_h+18, "#DCE5FF", rx=12, stroke="#1E3A8A", sw=1.2)
b.text(gx, y+pady+12, "CORE GOALS", 15, "#1E3A8A", "bold", ls="0.5")
for i, g in enumerate(goal):
    b.text(gx, y+pady+46+i*30, "✓", 17, "#1E3A8A", "bold")
    b.text(gx+22, y+pady+46+i*30, g, 17, "#334155")
```
Between consecutive lanes draw the connector:
```python
cx = P + laneL_w/2
b.arrow(cx, y_prev_bottom+4, y_next_top-2, "#0EA5C4")
b.node(cx, (y_prev_bottom+y_next_top)/2, label="↓")
```
**Palette tip:** give the three lanes three solid colors stepping along one hue family
(indigo → blue → teal) to simulate the "funnel progression" a gradient would have done.

---

## 2. Pipeline (horizontal) — best for a clean left→right flow, light detail per step
Equal step boxes in a row, connected by native arrows. Optional caption under each box.
Use when the *sequence* matters more than per-step depth.
```python
steps = ["Intake","Validate","Fulfill","Review","Disclose"]
n = len(steps); gap = 40
bw = (b.W - 2*b.P - (n-1)*gap) / n
y, h = 240, 90
for i, s in enumerate(steps):
    x = b.P + i*(bw+gap)
    b.card(x, y, bw, h, fill="#1487C9")
    b.text(x+bw/2, y+h/2+7, s, 20, "#EAF6FF", "bold", "middle")
    if i < n-1:
        b.arrow(x+bw, y+h/2, x+bw+gap, y+h/2, "#0D4FA8")
```
For a step that fans out, use `b.polyline([(x,y),(x,y2),(x3,y2)])` for a right-angled connector.

---

## 3. Comparison grid — best for weighing 2–3 options on shared criteria
A header row of options, a left column of criteria, cells at the intersections. Parallel
structure is the whole point: same rows, judged side by side. Tint the recommended column.
```python
options = ["Legacy Tool", "New Platform"]
criteria = ["Workflow", "Audit trail", "Collaboration", "Tech debt"]
cells = [["Fragmented","Unified"], ["Weak","End-to-end"],
         ["Manual handoff","In-platform"], ["High","Replaced"]]
label_w = 240; ncol = len(options)
colw = (b.W - 2*b.P - label_w) / ncol
y, rh = 220, 64
for j, o in enumerate(options):                       # header
    x = b.P + label_w + j*colw
    fill = "#13877A" if j == ncol-1 else "#64748B"    # tint the recommended one
    b.card(x, y, colw-12, 52, fill=fill)
    b.text(x+(colw-12)/2, y+33, o, 19, "#FFFFFF", "bold", "middle")
for i, crit in enumerate(criteria):                   # rows
    ry = y + 60 + i*rh
    b.text(b.P+8, ry+rh/2+6, crit, 17, "#0F172A", "bold")
    for j in range(ncol):
        x = b.P + label_w + j*colw
        rec = (j == ncol-1)
        b.rect(x, ry, colw-12, rh-10, "#D2F3EC" if rec else "#F1F5F9",
               rx=8, stroke="#99E0D2" if rec else "#E2E8F0", sw=1)
        b.text(x+(colw-12)/2, ry+(rh-10)/2+6, cells[i][j], 16,
               "#0B5F54" if rec else "#334155", "regular", "middle")
```

---

## 4. System map — best for components of one system and how they connect
Boxes placed by topology (tiers, hub-and-spoke, or core+satellites), wired with native
connectors. Group related boxes with a low-key background band. Keep arrows straight or
right-angled so they map to clean connectors.
```python
# tiered example: a row of clients → a gateway → a row of services
def box(x, y, w, h, label, fill, tx="#FFFFFF"):
    b.card(x, y, w, h, fill=fill); b.text(x+w/2, y+h/2+6, label, 18, tx, "bold", "middle")

b.rect(b.P, 200, b.W-2*b.P, 120, "#EAF1FF", rx=14)            # tier band (solid, not opacity)
box(120, 230, 180, 60, "Web Client", "#2A4BC4")
box(330, 230, 180, 60, "Mobile Client", "#2A4BC4")
box(720, 360, 220, 70, "API Gateway", "#1487C9")             # mid tier
for sx in (120, 330):
    b.polyline([(sx+90, 290), (sx+90, 330), (830, 330), (830, 360)], "#0D4FA8")
```
Use `b.node()` for a labeled junction, and a small solid diamond only as a rare accent
(polygons rasterize — don't make them structural).

---

## 5. Timeline — best for milestones over time
A horizontal (or vertical) spine with dated nodes; alternate captions above/below to avoid
collisions.
```python
spine_y = 320
b.rect(b.P, spine_y-2, b.W-2*b.P, 4, "#1487C9")              # spine
events = [("Q1","Onboard first datasets"), ("Q2","Cut processing SLA"),
          ("Q3","Launch new workspace"), ("Q4","Admin console GA")]
step = (b.W - 2*b.P) / (len(events))
for i, (t, label) in enumerate(events):
    cx = b.P + step*(i+0.5)
    b.node(cx, spine_y, r=14, label="", ring="#0EA5C4", fill="#FFFFFF")
    up = i % 2 == 0
    ty = spine_y - 70 if up else spine_y + 40
    b.rect(cx-110, ty, 220, 56, "#F1F5F9", rx=10, stroke="#E2E8F0", sw=1)
    b.text(cx, ty+24, t, 16, "#0B5C8A", "bold", "middle")
    b.text(cx, ty+44, label, 15, "#334155", "regular", "middle")
```

---

## 6. Card grid — best for a flat set of peers (features, principles, team pods)
Even tiles in an N-column grid; each tile a small title + a line of body. No false hierarchy.
```python
items = [("Auth Service","Identity & SSO for all channels"),
         ("Notification","Email / SMS / push delivery"),
         ("Analytics","Volume, SLA and trend metrics"),
         ("Audit Log","Cross-team trail & governance")]
ncol = 4; gap = 16; y = 240
cw = (b.W - 2*b.P - (ncol-1)*gap) / ncol
for i, (t, d) in enumerate(items):
    x = b.P + (i % ncol)*(cw+gap)
    b.card(x, y, cw, 96, fill="#21324F", rx=12)
    b.text(x+16, y+30, t, 17, "#5EEAD4", "bold")
    for k, ln in enumerate(wrap(d, cw-32, 15)):
        b.text(x+16, y+54+k*20, ln, 15, "#CBD5E1")
```

---

## Add-ons (compose onto any archetype)

**Title block** (top-left): a big solid-color title + a muted subtitle. Title ≥ 40px.
```python
b.text(b.P, 70, "Acme Product Map", 46, "#1E3A8A", "bold")
b.text(b.P, 104, "From request intake → processing → resolution", 18, "#475569")
```

**Context bar**: a row of fact pills under the title — great for definitions/scope without a
"homework header" (keep it factual, not meta about the task).
```python
y = 150; cx = b.P
for c in ["Internal tool platform", "Built on shared services", "Serves Web / Mobile / API"]:
    w = text_w(c, 16) + 28
    b.rect(cx, y, w, 38, "#FFFFFF", rx=9, stroke="#D6E4F5", sw=1.2)
    b.text(cx+14, y+24, c, 16, "#334155"); cx += w + 10
```

**Pain / status strip**: a tinted dashed band of issues — pairs well with each swimlane.
```python
b.rect(x, py, strip_w, 34, "#FBEAEA", rx=9, stroke="#F0C4C4", sw=1.4, dash="6 5")
b.text(x+16, py+22, "PAIN", 15, "#D11F44", "bold", ls="1")
# then b.chip(...) each issue in white pills
```

**Base dock**: a full-width dark band beneath everything for the layer that underpins the
rest (dependencies, platform). Use the **card grid** recipe inside it.

**Throughline pill** (top-right): the one-line narrative, e.g.
`Submit Better → Fulfill Faster → Handle In One Place`, arrows in the accent color.

---

## The overflow-safety habit
The single discipline that keeps boards clean: **measure, size, then draw.** For any container
that holds wrapping text or chips, call `b.chips_height(...)` (or `wrap(...)` and count lines)
first, size the card/lane to that height, *then* draw the contents into it. Containers grow to
content; text never gets fit-to-the-pixel. If `--check` still reports a `text-overflow`, the
usual cause is a single chip whose label is wider than its column — shorten the label or drop
that column's font by 1px, don't shrink the whole board.
