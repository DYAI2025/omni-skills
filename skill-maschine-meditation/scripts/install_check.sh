#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-maschine-meditation}"

test -f "$ROOT/SKILL.md" || { echo "SKILL.md fehlt"; exit 1; }
test -d "$ROOT/references" || { echo "references/ fehlt"; exit 1; }
test -d "$ROOT/assets/prompts" || { echo "assets/prompts/ fehlt"; exit 1; }
test -d "$ROOT/assets/templates" || { echo "assets/templates/ fehlt"; exit 1; }

echo "Struktur OK: $ROOT"
