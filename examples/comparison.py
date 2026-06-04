#!/usr/bin/env python3
"""Comparison grid archetype — weigh options on shared criteria; tint the pick.
Fictional content. Run: python3 examples/comparison.py  ->  /tmp/comparison.svg"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from board import Board, text_w

b = Board(width=1680)
P, W = b.P, b.W
b.text(P, 70, "Build vs Buy — Internal Analytics", 42, "#1B3858", "bold")
b.text(P, 104, "Same criteria, judged side by side. Recommended column tinted.", 18, "#475569")

options = ["Build in-house", "Buy SaaS"]
criteria = ["Time to launch", "Upfront cost", "Customization", "Maintenance", "Data control"]
cells = [["6+ months","2–4 weeks"],
         ["High (eng time)","Subscription"],
         ["Unlimited","Vendor-bound"],
         ["Our team owns it","Vendor handles"],
         ["Full","Shared / external"]]
rec = 1  # recommended column index (Buy)

label_w = 300; ncol = len(options)
colw = (W - 2*P - label_w) / ncol
y, rh = 200, 76
for j, o in enumerate(options):
    x = P + label_w + j*colw
    fill = "#13877A" if j == rec else "#64748B"
    b.card(x, y, colw-16, 58, fill=fill)
    b.text(x+(colw-16)/2, y+37, o, 21, "#FFFFFF", "bold", "middle")
for i, crit in enumerate(criteria):
    ry = y + 70 + i*rh
    b.rect(P, ry, label_w-12, rh-12, "#F1F5F9", rx=8, stroke="#E2E8F0", sw=1)
    b.text(P+16, ry+(rh-12)/2+6, crit, 17, "#0F172A", "bold")
    for j in range(ncol):
        x = P + label_w + j*colw
        is_rec = (j == rec)
        b.rect(x, ry, colw-16, rh-12, "#D2F3EC" if is_rec else "#FFFFFF",
               rx=8, stroke="#99E0D2" if is_rec else "#E2E8F0", sw=1.2)
        b.text(x+(colw-16)/2, ry+(rh-12)/2+6, cells[i][j], 17,
               "#0B5F54" if is_rec else "#334155", "bold" if is_rec else "regular", "middle")

# verdict band
vy = y + 70 + len(criteria)*rh + 12
b.rect(P+label_w, vy, (W-2*P-label_w), 52, "#0B5F54", rx=10)
b.text(P+label_w+20, vy+33, "Verdict: Buy now to launch this quarter; revisit build if customization needs grow.",
       17, "#E6FBF5", "bold")
b.save("/tmp/comparison.svg")
print("wrote /tmp/comparison.svg")
