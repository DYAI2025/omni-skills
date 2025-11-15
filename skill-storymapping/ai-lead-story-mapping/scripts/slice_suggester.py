#!/usr/bin/env python3
"""
Slice Suggester

Erzeugt einfache Vorschläge für vertikale Slices aus einer Story-Map-JSON.

Heuristik:
- MVP (Slice 1) = Walking Skeleton: pro Aktivität pro Step die erste passende Story (falls vorhanden)
- Reststories werden gleichmäßig auf Slice 2/3 verteilt
"""
import sys
import json
import math
from collections import defaultdict


def main():
    if len(sys.argv) < 2:
        print("Usage: slice_suggester.py <story_map.json> [--out slices.md]", file=sys.stderr)
        sys.exit(1)
    
    path = sys.argv[1]
    out = None
    
    # Parse --out Option
    if "--out" in sys.argv:
        i = sys.argv.index("--out")
        if i + 1 < len(sys.argv):
            out = sys.argv[i + 1]
    
    # JSON laden
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[slice-suggester] ERROR: Kann JSON nicht lesen: {e}", file=sys.stderr)
        sys.exit(1)
    
    activities = data.get("activities", [])
    stories = data.get("stories", [])
    
    # Index Stories per step
    by_step = defaultdict(list)
    for st in stories:
        by_step[st["step_id"]].append(st)
    
    # MVP: für jeden Step der Aktivität die erste Story (falls vorhanden)
    mvp_ids = set()
    mvp_list = []
    
    for a in activities:
        for s in a["steps"]:
            candidates = by_step.get(s["id"], [])
            if candidates:
                pick = candidates[0]
                if pick["id"] not in mvp_ids:
                    mvp_ids.add(pick["id"])
                    mvp_list.append(pick)
    
    # Reststories
    rest = [st for st in stories if st["id"] not in mvp_ids]
    
    # Aufteilen in 2-3 Slices (je nach Größe)
    if len(rest) == 0:
        rest_slices = []
    elif len(rest) <= 8:
        chunks = 2
    else:
        chunks = 3
    
    size = math.ceil(len(rest) / chunks) if rest else 0
    rest_slices = [rest[i:i + size] for i in range(0, len(rest), size)] if rest else []
    
    # Markdown generieren
    md = []
    md.append("# Slice‑Vorschläge\n")
    md.append(f"**Produkt:** {data.get('product', 'N/A')}")
    md.append(f"**Goal:** {data.get('goal', 'N/A')}\n")
    
    md.append("## Slice 1 – MVP (Walking Skeleton)\n")
    md.append("**Ziel:** End-to-End nutzbare Complete Product Experience\n")
    
    if mvp_list:
        for st in mvp_list:
            md.append(f"- **{st['id']}**: {st['title']} (activity={st['activity_id']}, step={st['step_id']})")
    else:
        md.append("- <keine Stories>")
    
    md.append("")
    
    # Folge-Slices
    for idx, sl in enumerate(rest_slices, start=2):
        md.append(f"## Slice {idx}\n")
        md.append(f"**Ziel:** Weitere Features und Alternativen\n")
        
        if sl:
            for st in sl:
                md.append(f"- **{st['id']}**: {st['title']} (activity={st['activity_id']}, step={st['step_id']})")
        else:
            md.append("- <keine Stories>")
        
        md.append("")
    
    # Hinweise
    md.append("---\n")
    md.append("**Hinweise:**")
    md.append("- Slice 1 (MVP) enthält mind. 1 Story pro kritischem Backbone-Schritt")
    md.append("- Folge-Slices fügen 'Fleisch' hinzu: Alternativen, Komfort, Optimierungen")
    md.append("- Jede Slice sollte mit Outcomes/Metriken versehen werden")
    md.append("- Dependencies zwischen Stories beachten!")
    
    text = "\n".join(md)
    
    # Output
    if out:
        with open(out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[slice-suggester] ✓ Geschrieben: {out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
