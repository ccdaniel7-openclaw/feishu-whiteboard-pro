#!/usr/bin/env python3
"""
board.py — Feishu whiteboard generator toolkit.

Why this exists: the Feishu SVG board is a "rectangles, circles, lines and text"
medium with hard limits (no gradients / filters / opacity, one font, native arrows
only — see RULES.md). Hand-writing hundreds of <rect>/<text> with pixel coordinates
is slow and error-prone, and the #1 defect is text overflowing its box because CJK
and Latin glyphs have very different widths. This library does the arithmetic for you:
it measures text, wraps chips, grows containers to fit their content, and emits a
board-legal SVG. You compose layout by calling these primitives; COMPONENTS.md shows
the recipes (swimlane, comparison, pipeline, system map, timeline, card grid).

Import it:  from board import Board
Then:       b = Board(width=1680); ... ; b.save("diagram.svg")

Everything here is deliberately board-legal: solid fills only, marker-end arrows,
type defaults >= 16px. Don't reach around it to add a gradient or a blur — the board
will silently flatten the whole node to a lumpy raster image.
"""
import html

# ----- text measurement -------------------------------------------------------
# The board hardcodes one font; we approximate advance width per glyph. CJK ~= 1em,
# Latin ~= 0.58em. This is the single most useful thing in the file: it lets every
# container size itself so nothing clips.
def char_w(c, fs):
    return fs * (1.0 if ord(c) > 0x2E80 else 0.58)

def text_w(s, fs):
    return sum(char_w(c, fs) for c in s)

def wrap(s, max_w, fs):
    """Greedy word-wrap that respects max_w. Returns a list of lines."""
    out, cur = [], ""
    for word in s.split(" "):
        if not word:
            continue
        trial = (cur + " " + word).strip()
        if cur and text_w(trial, fs) > max_w:
            out.append(cur); cur = word
        else:
            cur = trial
    if cur:
        out.append(cur)
    return out or [""]


class Board:
    def __init__(self, width=1680, pad=50, bg="#F4F7FB"):
        self.W = width
        self.P = pad
        self.bg = bg
        self.parts = []
        self._max_y = 0  # tracks content extent so the canvas height auto-fits

    # -- low-level primitives --------------------------------------------------
    def _bump(self, y):
        self._max_y = max(self._max_y, y)

    def rect(self, x, y, w, h, fill, rx=0, stroke=None, sw=0, dash=None, z=None):
        s = f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"'
        if stroke: s += f' stroke="{stroke}" stroke-width="{sw}"'
        if dash:   s += f' stroke-dasharray="{dash}"'
        self.parts.append(s + '/>')
        self._bump(y + h)

    def text(self, x, y, s, fs=16, fill="#0F172A", weight="regular",
             anchor="start", ls=None, upper=False):
        t = html.escape(s.upper() if upper else s, quote=True)
        extra = f' letter-spacing="{ls}"' if ls else ''
        self.parts.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-size="{fs}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}"{extra}>{t}</text>')
        self._bump(y + fs * 0.3)

    def circle(self, cx, cy, r, fill, stroke=None, sw=0):
        s = f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}"'
        if stroke: s += f' stroke="{stroke}" stroke-width="{sw}"'
        self.parts.append(s + '/>')
        self._bump(cy + r)

    def arrow(self, x1, y1, x2, y2, color="#0D4FA8", sw=4, double=False):
        """A native connector. Keep it straight or right-angled (use polyline()).
        Arrowheads come from marker-end — NEVER draw a triangle yourself."""
        ms = ' marker-start="url(#arrow)"' if double else ''
        self.parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="{sw}"{ms} marker-end="url(#arrow)"/>')
        self._bump(max(y1, y2))

    def polyline(self, points, color="#0D4FA8", sw=4):
        """Right-angled connector. points = [(x,y),...]. Carries its own arrowhead."""
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
        self.parts.append(
            f'<polyline points="{pts}" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" marker-end="url(#arrow)"/>')
        self._bump(max(y for _, y in points))

    # -- composite helpers -----------------------------------------------------
    def chip(self, x, y, label, fs=16, h=32, pad=11, rx=8,
             fill="#EEF3F8", stroke="#D7E0EC", sw=1, tx="#1E293B", bold=False):
        """One pill. Returns its width so callers can place the next one."""
        w = text_w(label, fs) + 2 * pad
        self.rect(x, y, w, h, fill, rx=rx, stroke=stroke, sw=sw)
        self.text(x + w / 2, y + h / 2 + fs * 0.36, label, fs, tx,
                  "bold" if bold else "regular", "middle")
        return w

    def chips(self, x, y, items, max_w, fs=16, h=32, pad=11, gap_x=8, gap_y=9,
              fill="#EEF3F8", stroke="#D7E0EC", tx="#1E293B",
              key_fill=None, key_stroke=None, key_tx=None):
        """Auto-wrapping chip flow inside a column of width max_w.
        items: list of str, or (str, is_key) tuples. Key chips get the accent style.
        Returns the bottom y so the caller knows how tall the block grew."""
        cx, cy = x, y
        for it in items:
            label, is_key = (it if isinstance(it, tuple) else (it, False))
            w = text_w(label, fs) + 2 * pad
            if cx > x and cx + w > x + max_w:        # wrap
                cx = x; cy += h + gap_y
            if is_key:
                self.chip(cx, cy, label, fs, h, pad, 8,
                          key_fill or "#DCE5FF", key_stroke or "#1E3A8A", 1.4,
                          key_tx or "#1E3A8A", bold=True)
            else:
                self.chip(cx, cy, label, fs, h, pad, 8, fill, stroke, 1, tx)
            cx += w + gap_x
        return cy + h

    def chips_height(self, items, max_w, fs=16, h=32, pad=11, gap_x=8, gap_y=9):
        """Pre-compute the height chips() will occupy — use it to size containers
        BEFORE drawing, so the card/lane is exactly tall enough."""
        cx, rows = 0, 1
        for it in items:
            label = it[0] if isinstance(it, tuple) else it
            w = text_w(label, fs) + 2 * pad
            if cx > 0 and cx + w > max_w:
                rows += 1; cx = 0
            cx += w + gap_x
        return rows * (h + gap_y)

    def card(self, x, y, w, h, fill="#FFFFFF", rx=16, stroke=None, sw=0):
        self.rect(x, y, w, h, fill, rx=rx, stroke=stroke, sw=sw)

    def node(self, cx, cy, r=22, label="", fill="#FFFFFF", ring="#0EA5C4", fs=22):
        """Connector hub — a ringed circle with an optional glyph (e.g. an arrow)."""
        self.circle(cx, cy, r, fill, stroke=ring, sw=3)
        if label:
            self.text(cx, cy + fs * 0.36, label, fs, ring, "bold", "middle")

    # -- output ----------------------------------------------------------------
    def save(self, path, height=None):
        H = int(height if height else self._max_y + self.P)
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.W}" height="{H}" '
            f'viewBox="0 0 {self.W} {H}">'
            f'<defs><marker id="arrow" markerWidth="12" markerHeight="12" refX="9" refY="4" '
            f'orient="auto" markerUnits="strokeWidth"><path d="M0 0 L10 4 L0 8 z"/></marker></defs>'
            f'<rect x="0" y="0" width="{self.W}" height="{H}" fill="{self.bg}"/>'
            + "".join(self.parts) + '</svg>')
        with open(path, "w") as f:
            f.write(svg)
        return path, self.W, H
