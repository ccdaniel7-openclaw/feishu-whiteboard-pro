#!/usr/bin/env bash
# Preflight for feishu-whiteboard-pro: verifies everything needed to render an SVG locally
# and to write it into Feishu as an editable whiteboard.
set -u
ok=1
echo "▶ feishu-whiteboard-pro preflight"
echo

# Node >= 20
if command -v node >/dev/null 2>&1; then
  v=$(node -v); echo "  ✓ Node $v"
  major=$(echo "$v" | sed 's/v\([0-9]*\).*/\1/')
  [ "${major:-0}" -ge 20 ] || { echo "    ! Node >= 20 recommended"; }
else
  echo "  ✗ Node.js not found — install Node >= 20 (https://nodejs.org)"; ok=0
fi

# Python 3 (the generator)
if command -v python3 >/dev/null 2>&1; then
  echo "  ✓ $(python3 --version)"
else
  echo "  ✗ python3 not found — needed for scripts/board.py"; ok=0
fi

# lark-cli (auth + writing to Feishu)
if command -v lark-cli >/dev/null 2>&1; then
  echo "  ✓ lark-cli ($(lark-cli --version 2>/dev/null | head -1))"
  if lark-cli auth status 2>/dev/null | grep -q '"tokenStatus": *"valid"'; then
    echo "  ✓ lark-cli authenticated (token valid)"
  elif lark-cli auth status >/dev/null 2>&1; then
    echo "  ! lark-cli token needs refresh or re-auth. If pushes fail, run: lark-cli auth login"
  else
    echo "  ! lark-cli not authenticated. Run:"
    echo "        lark-cli auth login        # device-flow; scan the QR / open the URL"
  fi
else
  echo "  ✗ lark-cli not found. Install + authenticate:"
  echo "        npm install -g @larksuite/cli"
  echo "        lark-cli auth login"
  ok=0
fi

# whiteboard-cli via npx (render-only, no auth)
if npx -y @larksuite/whiteboard-cli@^0.2.11 -v >/dev/null 2>&1; then
  echo "  ✓ @larksuite/whiteboard-cli reachable via npx"
else
  echo "  ! could not reach @larksuite/whiteboard-cli via npx (needs network on first run)"
fi

echo
if [ "$ok" = 1 ]; then
  echo "✅ Ready. Boards write to your own Feishu/Lark tenant."
else
  echo "❌ Missing prerequisites above. Install them, then re-run."; exit 1
fi
