#!/usr/bin/env python3
"""Timeline archetype — milestones on a spine, captions alternating to avoid collisions.
Fictional content. Run: python3 examples/timeline.py  ->  /tmp/timeline.svg"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from board import Board, text_w, wrap

b = Board(width=1680)
P, W = b.P, b.W
b.text(P, 70, "2026 Product Roadmap", 42, "#0B5C8A", "bold")
b.text(P, 104, "Four quarters, one milestone each — alternating above/below the spine", 18, "#475569")

spine_y = 360
b.rect(P, spine_y-3, W-2*P, 6, "#1487C9", rx=3)
events = [("Q1","Onboard first datasets","Wire up the 3 priority sources"),
          ("Q2","Cut processing SLA 30%","Move pulls online, add queues"),
          ("Q3","Launch new workspace","Unified case view ships to beta"),
          ("Q4","Admin console GA","Self-serve org & role management")]
step = (W - 2*P) / len(events)
for i, (t, head, body) in enumerate(events):
    cx = P + step*(i+0.5)
    up = (i % 2 == 0)
    card_y = spine_y - 150 if up else spine_y + 40
    # connector node + stem
    b.circle(cx, spine_y, 16, "#FFFFFF", stroke="#0EA5C4", sw=4)
    stem_to = card_y+110 if up else card_y
    b.rect(cx-2, min(spine_y, stem_to), 4, abs(spine_y-stem_to), "#0EA5C4")
    # card
    cw = step-50
    b.card(cx-cw/2, card_y, cw, 110, "#FFFFFF", rx=12, stroke="#CFE0F0", sw=1.4)
    b.rect(cx-cw/2, card_y, cw, 36, "#1487C9", rx=12)
    b.text(cx-cw/2+16, card_y+24, t, 16, "#EAF6FF", "bold")
    b.text(cx-cw/2+16, card_y+60, head, 18, "#0F172A", "bold")
    for k, ln in enumerate(wrap(body, cw-32, 15)):
        b.text(cx-cw/2+16, card_y+84+k*20, ln, 15, "#475569")
b.save("/tmp/timeline.svg")
print("wrote /tmp/timeline.svg")
