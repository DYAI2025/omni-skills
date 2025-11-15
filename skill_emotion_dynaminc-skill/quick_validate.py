#!/usr/bin/env python3
import sys
from pathlib import Path

REQUIRED_FILES = [
    "SKILL.md",
    "references/emotion-dynamics-quick-notes.md",
]

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: quick_validate.py <skill_dir>")
        return 2

    base = Path(sys.argv[1])
    if not base.is_dir():
        print(f"ERROR: '{base}' not found or not a directory")
        return 1

    ok = True
    for rel in REQUIRED_FILES:
        p = base / rel
        if not p.is_file():
            print(f"MISSING: {p}")
            ok = False
        else:
            print(f"OK: {p}")

    # Light content checks
    skill = base / "SKILL.md"
    if skill.is_file():
        text = skill.read_text(encoding="utf-8", errors="ignore")
        required_markers = ["name:", "description:", "## Workflow/Anweisungen", "## Ausgabeformat"]
        for marker in required_markers:
            if marker not in text:
                print(f"WARN: '{marker}' not found in SKILL.md")
        else:
            print("Content check: SKILL.md markers scanned.")

    print("Validation:", "PASS" if ok else "FAIL")
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())

