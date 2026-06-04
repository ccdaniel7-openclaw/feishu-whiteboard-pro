#!/usr/bin/env python3
"""Pipeline archetype — a clean left→right flow with light per-step detail.
Fictional content. Run: python3 examples/pipeline.py  ->  /tmp/pipeline.svg"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from board import Board, text_w, wrap

b = Board(width=1680)
P, W = b.P, b.W
b.text(P, 70, "Content Publishing Pipeline", 42, "#16608F", "bold")
b.text(P, 104, "From idea to published — each stage owns one job", 18, "#475569")

steps = [("Draft","Writer drafts in the editor"),
         ("Review","Editor checks facts & tone"),
         ("Design","Visuals & layout added"),
         ("Approve","Owner signs off"),
         ("Publish","Goes live + notify")]
n = len(steps); gap = 44
bw = (W - 2*P - (n-1)*gap) / n
y, h = 230, 96
for i, (s, cap) in enumerate(steps):
    x = P + i*(bw+gap)
    b.card(x, y, bw, h, fill="#2D8FE0")
    b.text(x+bw/2, y+44, f"{i+1}", 20, "#D7EAFB", "bold", "middle")
    b.text(x+bw/2, y+74, s, 22, "#FFFFFF", "bold", "middle")
    for k, ln in enumerate(wrap(cap, bw-20, 16)):
        b.text(x+bw/2, y+h+28+k*22, ln, 16, "#334155", "regular", "middle")
    if i < n-1:
        b.arrow(x+bw, y+h/2, x+bw+gap, y+h/2, "#16608F")

# a feedback loop (right-angled connector) from Review back to Draft
x_review = P + 1*(bw+gap); x_draft = P + 0*(bw+gap)
b.polyline([(x_review+bw/2, y), (x_review+bw/2, y-46),
            (x_draft+bw/2, y-46), (x_draft+bw/2, y)], "#D11F44")
b.text((x_draft+x_review)/2 + bw/2, y-56, "rework loop", 15, "#D11F44", "bold", "middle")

b.save("/tmp/pipeline.svg")
print("wrote /tmp/pipeline.svg")
