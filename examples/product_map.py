#!/usr/bin/env python3
"""
Worked example: a 3-lane product map using the Swimlane archetype + add-ons
(title, context bar, throughline pill, per-lane pain strip, base dock).

Fictional product ("Acme Helpdesk Platform") — generic, no real data. It exists to show
the recipe end-to-end. Swap the LANES content for your own.

Run:  python3 examples/product_map.py   ->  writes /tmp/product_map.svg
Then: scripts/render_check.sh /tmp/product_map.svg
Palette: Riptide (see references/palettes.md).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from board import Board, text_w, wrap

b = Board(width=1680)
P, W = b.P, b.W
INK, SUB, CYAN = "#0F172A", "#475569", "#0EA5C4"

LANES = [
 dict(tag="STAGE 01 · INTAKE", name="Portal", role="Capture Better",
      fill="#2A4BC4", txt="#EBF1FF", posbg="#3D5CCB", light="#DCE5FF", lk="#1E3A8A",
      pos="Unified entry for inbound requests — submission UX and status updates",
      owners=["Web / Email / API · Team Alpha"],
      cols=[("Channels", ["Web","Email","API","Mobile"]),
            ("Capabilities", ["Sign-up / SSO","Multi-language","Request Form","Attachments","Status Notify"]),
            ("Key Needs", [("Submission UX",1),("SSO",0),("Localization",0),("Attachment rules",0)])],
      goal=["Higher request quality","Fewer follow-up loops","Less friction for requesters"],
      pain=["Sign-up friction","Localization gaps","Attachment rules","Notification noise"]),
 dict(tag="STAGE 02 · PROCESSING", name="Engine", role="Process Faster",
      fill="#1487C9", txt="#EAF6FF", posbg="#3098D2", light="#D6EEFB", lk="#0B5C8A",
      pos="Validation, enrichment and routing — turns raw requests into work items",
      owners=["Pipeline & Rules · Team Beta"],
      cols=[("Mandate", ["Validate","Enrich","Classify","Route"]),
            ("Capabilities", ["Rules Engine","Dedup","Priority","Queues","Webhooks","SLA Timers"]),
            ("Key Needs", [("Auto-classification",1),("Dedup at intake",0),("Priority routing",0)])],
      goal=["Lower processing latency","Higher routing accuracy","More automated coverage"],
      pain=["Manual triage","Long queue waits","Misroutes","Rule sprawl"]),
 dict(tag="STAGE 03 · DELIVERY", name="Workspace", role="Resolve In One Place",
      fill="#13877A", txt="#E6FBF5", posbg="#2E9788", light="#D2F3EC", lk="#0B5F54",
      pos="The agent workspace for handling and collaboration — one source of truth",
      owners=["Case & Collaboration · Team Gamma"],
      cols=[("Mandate", ["Case Mgmt","Transfer & Collab","SLA","Audit & Trail"]),
            ("Collaborators", ["Agents","Ops","QA","Specialists"]),
            ("Key Needs", [("Unified case view",1),("My Tasks",0),("On Hold",0),("Handover notes",0),("Quality Score",0)])],
      goal=["Unify flow & states","Clear ownership","End-to-end audit trail"],
      pain=["Fragmented tools","Weak handover trail","Inconsistent statuses","No audit"]),
]

laneL_w = 300; laneR_x = P + laneL_w; laneR_w = W - P - laneR_x
padx, pady, gap = 28, 22, 22
col_w = (laneR_w - 2*padx - 3*gap) / 4

# ---- title + subtitle ----
b.text(P, 70, "Acme Helpdesk Platform — Product Map", 42, "#1E3A8A", "bold")
b.text(P, 104, "An end-to-end chain — from request intake, to processing, to resolution", 18, SUB)
# ---- throughline pill (top-right) ----
segs = ["Capture Better","→","Process Faster","→","Resolve In One Place"]
pill_w = text_w("THROUGHLINE          Capture Better    →    Process Faster    →    Resolve In One Place", 16) + 44
px = W - P - pill_w
b.rect(px, 44, pill_w, 44, "#FFFFFF", rx=12, stroke="#D2E1F3", sw=1.4)
tx = px + 22
b.text(tx, 71, "THROUGHLINE", 14, "#1E3A8A", "bold", ls="1"); tx += text_w("THROUGHLINE",14)+24
for s in segs:
    b.text(tx, 72, s, 16, CYAN if s=="→" else INK, "bold"); tx += text_w(s,16)+16
# ---- context bar ----
y = 138
cx = P
for c in ["A fictional example platform","Cool 'Riptide' palette","Serves Web / Email / API + internal teams","Intake → Processing → Delivery"]:
    w = text_w(c,16)+28
    b.rect(cx, y, w, 38, "#FFFFFF", rx=9, stroke="#D6E4F5", sw=1.2)
    b.text(cx+14, y+24, c, 16, "#334155"); cx += w+10
y += 38+20
# ---- entry marker ----
b.rect(P, y, 130, 60, "#7E8AA0", rx=14)
b.text(P+65, y+27, "Inbound", 15, "#FFFFFF", "bold", "middle")
b.text(P+65, y+46, "Requests", 15, "#FFFFFF", "bold", "middle")
b.text(P+150, y+26, "Web / Email / API", 20, INK, "bold")
b.text(P+150, y+48, "Submit requests into the chain", 16, SUB)
b.arrow(P+150+330, y+8, P+150+330, y+56, CYAN)
y += 60+18

conn = []
for L in LANES:
    content_h = max([28 + b.chips_height(items, col_w) for _, items in L["cols"]]
                    + [28 + len(L["goal"])*30])
    pos_lines = wrap(L["pos"], laneL_w-60, 15)
    leftH = 32+38+26+22 + (12+len(pos_lines)*22) + 18+20 + len(L["owners"])*20 + 20
    pain_h = 46
    lane_h = max(pady*2 + content_h + 14 + pain_h, leftH, 200)
    ly0 = y
    # left rail
    b.card(P, ly0, laneL_w, lane_h, fill=L["fill"])
    ly = ly0+32
    b.text(P+26, ly, L["tag"], 13, L["txt"], "bold"); ly += 38
    b.text(P+26, ly, L["name"], 32, L["txt"], "bold"); ly += 26
    b.text(P+26, ly, L["role"], 17, L["txt"], "bold"); ly += 22
    pos_h = 12+len(pos_lines)*22
    b.rect(P+22, ly, laneL_w-44, pos_h, L["posbg"], rx=8)
    b.rect(P+22, ly, 4, pos_h, "#FFFFFF")
    for i, ln in enumerate(pos_lines): b.text(P+36, ly+24+i*22, ln, 15, L["txt"])
    ly += pos_h+18
    b.text(P+26, ly, "OWNERS", 12, L["txt"], "bold", ls="1"); ly += 20
    for ln in L["owners"]: b.text(P+26, ly, ln, 14, L["txt"]); ly += 20
    # detail area
    b.card(laneR_x, ly0, laneR_w, lane_h, fill="#FFFFFF")
    cx0 = laneR_x+padx; cy0 = ly0+pady
    for i, (h4, items) in enumerate(L["cols"]):
        x = cx0 + i*(col_w+gap)
        b.text(x, cy0+12, h4, 15, "#94A3B8", "bold", ls="0.5", upper=True)
        b.chips(x, cy0+28, items, col_w, key_fill=L["light"], key_stroke=L["lk"], key_tx=L["lk"])
    gx = cx0 + 3*(col_w+gap); goal_h = 28+len(L["goal"])*30
    b.rect(gx-12, cy0-6, col_w+18, goal_h+18, L["light"], rx=12, stroke=L["lk"], sw=1.2)
    b.text(gx, cy0+12, "Core Goals", 15, L["lk"], "bold", ls="0.5", upper=True)
    for i, g in enumerate(L["goal"]):
        gyy = cy0+46+i*30
        b.text(gx, gyy, "✓", 17, L["lk"], "bold"); b.text(gx+22, gyy, g, 17, "#334155")
    # pain strip
    py = ly0+lane_h-pady-pain_h+10
    b.rect(cx0, py, laneR_w-2*padx, pain_h-12, "#FBEAEA", rx=9, stroke="#F0C4C4", sw=1.4, dash="6 5")
    ppx = cx0+16; pcy = py+(pain_h-12)/2
    b.text(ppx, pcy+6, "PAIN", 15, "#D11F44", "bold", ls="1"); ppx += text_w("PAIN",15)+24
    for p in L["pain"]:
        w = text_w(p,16)+20
        b.rect(ppx, pcy-15, w, 30, "#FFFFFF", rx=7, stroke="#F0C4C4", sw=1.1)
        b.text(ppx+w/2, pcy+5, p, 16, "#9F1239", "regular", "middle"); ppx += w+10
    conn.append((P+laneL_w/2, ly0, ly0+lane_h))
    y = ly0+lane_h+30

for i in range(len(LANES)-1):
    cxx = P+laneL_w/2; y1 = conn[i][2]; y2 = conn[i+1][1]
    b.arrow(cxx, y1+4, cxx, y2-2, CYAN)
    b.node(cxx, (y1+y2)/2, label="↓")

# ---- base dock (card grid inside a dark band) ----
deps = [("Auth Service","Identity & SSO for all channels"),("Notification","Email / SMS / push delivery"),
        ("Analytics","Volume, SLA and trend metrics"),("Audit Log","Cross-team trail & governance")]
base_h = 188
b.rect(P, y, W-2*P, base_h, "#14233F", rx=16)
b.rect(P+30, y+26, 6, 24, "#5EEAD4", rx=3)
b.text(P+46, y+45, "Shared Services & Dependencies", 22, "#FFFFFF", "bold")
dep_w = (W-2*P-60-3*16)/4
for i,(t,d) in enumerate(deps):
    dx = P+30+i*(dep_w+16); dyy = y+66
    b.rect(dx, dyy, dep_w, 76, "#21324F", rx=12)
    b.text(dx+16, dyy+28, t, 16, "#5EEAD4", "bold")
    for k, ln in enumerate(wrap(d, dep_w-32, 15)): b.text(dx+16, dyy+50+k*20, ln, 15, "#CBD5E1")
b.text(W/2, y+base_h-18, "Product direction:  Smoother intake · Faster processing · Unified resolution", 16, "#9FB3CC", "regular", "middle")

out = b.save("/tmp/product_map.svg")
print("wrote", out)
