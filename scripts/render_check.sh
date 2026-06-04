#!/usr/bin/env bash
# Render an SVG to PNG and run the geometric check in one call.
# Usage: scripts/render_check.sh <diagram.svg> [out.png]
# Then OPEN the PNG and look — the check catches overflow/overlap, but your eyes catch the rest.
set -u
SVG="${1:?usage: render_check.sh <diagram.svg> [out.png]}"
PNG="${2:-${SVG%.svg}.png}"
CLI="@larksuite/whiteboard-cli@^0.2.11"

echo "▶ rendering $SVG → $PNG"
npx -y "$CLI" -i "$SVG" -o "$PNG" -f svg >/dev/null 2>/tmp/_wb_render.err \
  && echo "  ✓ rendered" || { echo "  ✗ render failed:"; tail -5 /tmp/_wb_render.err; exit 1; }

echo "▶ geometric check (text-overflow / node-overlap)"
npx -y "$CLI" -i "$SVG" -f svg --check 2>&1 \
  | grep -iE '"errors"|"warnings"|textOverflow|nodeOverlap|"message"' \
  | sed 's/^/  /' || true

echo
echo "Now OPEN $PNG and look: text spilling out of boxes, a chip wider than its column,"
echo "content flush to the edge, accidental overlaps, anything clipped right/bottom. Fix, re-run."
