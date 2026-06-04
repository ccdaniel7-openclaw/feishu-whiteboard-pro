#!/usr/bin/env python3
"""System map archetype — tiered architecture wired with native connectors.
Fictional content. Run: python3 examples/system_map.py  ->  /tmp/system_map.svg"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from board import Board, text_w, wrap

b = Board(width=1680)
P, W = b.P, b.W
LINK = "#0D4FA8"
b.text(P, 70, "Order System — Architecture Map", 42, "#1E3A8A", "bold")
b.text(P, 104, "Clients → Gateway → Services → Data, with key dependencies", 18, "#475569")

def box(x, y, w, h, label, fill, tx="#FFFFFF", sub=None):
    b.card(x, y, w, h, fill=fill)
    if sub:
        b.text(x+w/2, y+h/2-2, label, 18, tx, "bold", "middle")
        b.text(x+w/2, y+h/2+20, sub, 13, tx, "regular", "middle")
    else:
        b.text(x+w/2, y+h/2+6, label, 18, tx, "bold", "middle")

inner = W - 2*P
# tier bands (solid, low-key)
def band(y, h, label):
    b.rect(P, y, inner, h, "#EAF1FF", rx=14)
    b.text(P+18, y+26, label, 14, "#1E3A8A", "bold", ls="0.5")

band(170, 110, "CLIENTS");   cy1 = 200
band(300, 110, "GATEWAY");   cy2 = 330
band(430, 130, "SERVICES");  cy3 = 460
# data tier as dark dock
b.rect(P, 590, inner, 120, "#14233F", rx=14)
b.text(P+18, 616, "DATA", 14, "#5EEAD4", "bold", ls="0.5")

# clients
clients = ["Web","iOS","Android"]
cw = 200; cx0 = (W - (len(clients)*cw + (len(clients)-1)*30))/2
for i, c in enumerate(clients):
    box(cx0+i*(cw+30), cy1, cw, 60, c, "#2A4BC4")
# gateway (center)
gw_w = 260; gw_x = (W-gw_w)/2
box(gw_x, cy2, gw_w, 60, "API Gateway", "#1487C9", sub="auth · routing · rate-limit")
# services row = 3 internal services + 1 external (PSP), evenly spaced so nothing collides
svcs = ["Order Service", "Inventory Service", "Payment Service"]
ncell = len(svcs) + 1                      # reserve the 4th slot for the external gateway
sw = 300; gap = (inner - ncell*sw)/(ncell-1)
sx = [P + i*(sw+gap) for i in range(ncell)]
for i, s in enumerate(svcs):
    box(sx[i], cy3, sw, 70, s, "#13877A")
# external PSP occupies the 4th slot — gray = outside our system
box(sx[3], cy3, sw, 70, "3rd-party PSP", "#7E8AA0", sub="external gateway")
# data
data = [("MySQL","orders"),("Redis","cache"),("Kafka","events")]
dw = 360; dgap = (inner - len(data)*dw)/(len(data)-1)
for i,(d,role) in enumerate(data):
    dx = P + i*(dw+dgap)
    b.rect(dx, 636, dw, 56, "#21324F", rx=10)
    b.text(dx+18, 670, d, 17, "#5EEAD4", "bold")
    b.text(dx+18+text_w(d,17)+14, 670, role, 14, "#CBD5E1")

# connectors: clients -> gateway
for i in range(len(clients)):
    x = cx0+i*(cw+30)+cw/2
    b.polyline([(x, cy1+60), (x, cy2-16), (gw_x+gw_w/2, cy2-16), (gw_x+gw_w/2, cy2)], LINK)
# gateway -> internal services only (fan out)
for i in range(len(svcs)):
    cxx = sx[i]+sw/2
    b.polyline([(gw_x+gw_w/2, cy2+60), (gw_x+gw_w/2, cy3-18), (cxx, cy3-18), (cxx, cy3)], LINK)
# internal services -> data
for i in range(len(svcs)):
    cxx = sx[i]+sw/2
    b.arrow(cxx, cy3+70, cxx, 590, "#0EA5C4")
# dependency notes (colored connectors + chips)
b.polyline([(sx[0]+sw, cy3+35), (sx[1], cy3+35)], "#D11F44")
b.rect(sx[0]+sw-6, cy3+18, text_w("checks stock",15)+18, 30, "#FBEAEA", rx=7, stroke="#F0C4C4", sw=1.1)
b.text(sx[0]+sw+3+ (text_w("checks stock",15)+6)/2, cy3+38, "checks stock", 15, "#9F1239", "regular", "middle")
# Payment -> external PSP (adjacent slots, clean horizontal hop)
b.arrow(sx[2]+sw, cy3+35, sx[3], cy3+35, "#C2410C")

b.save("/tmp/system_map.svg")
print("wrote /tmp/system_map.svg")
