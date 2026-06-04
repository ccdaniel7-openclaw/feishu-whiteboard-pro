#!/usr/bin/env python3
"""Card grid archetype — a flat set of peers, even tiles, no false hierarchy.
Fictional content. Run: python3 examples/card_grid.py  ->  /tmp/card_grid.svg"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from board import Board, text_w, wrap

b = Board(width=1680)
P, W = b.P, b.W
b.text(P, 70, "Engineering Principles", 42, "#1B3858", "bold")
b.text(P, 104, "Six peers, equal weight — the team's working agreements", 18, "#475569")

items = [("Ship small","Prefer many small, reversible changes over big-bang releases."),
         ("Own it end-to-end","If you build it, you run it — including on-call and metrics."),
         ("Write it down","Decisions live in docs, not in heads or DMs."),
         ("Automate the boring","If you did it twice by hand, script it the third time."),
         ("Measure, then tune","No perf claim without a number before and after."),
         ("Default to open","Share work-in-progress early; ask for review often.")]
ncol = 3; gap = 22; y = 180
cw = (W - 2*P - (ncol-1)*gap) / ncol
ch = 150
accents = ["#2A4BC4","#1487C9","#13877A","#7C3AED","#C2410C","#0B6E6E"]
for i, (t, d) in enumerate(items):
    row, col = divmod(i, ncol)
    x = P + col*(cw+gap); yy = y + row*(ch+gap)
    b.card(x, yy, cw, ch, "#FFFFFF", rx=14, stroke="#E2E8F0", sw=1.4)
    b.rect(x, yy, 8, ch, accents[i], rx=4)              # left accent stripe
    b.circle(x+44, yy+44, 20, accents[i]); b.text(x+44, yy+51, str(i+1), 18, "#FFFFFF", "bold", "middle")
    b.text(x+78, yy+51, t, 21, "#0F172A", "bold")
    for k, ln in enumerate(wrap(d, cw-110, 16)):
        b.text(x+78, yy+84+k*24, ln, 16, "#475569")
b.save("/tmp/card_grid.svg")
print("wrote /tmp/card_grid.svg")
