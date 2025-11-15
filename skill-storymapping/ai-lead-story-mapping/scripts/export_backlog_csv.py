#!/usr/bin/env python3
"""
Export Backlog CSV

Exportiert Stories aus story_map.json in eine Backlog-CSV.

Spalten:
id,title,description,depends_on,actor,goal,activity,step,pattern,effort,reach,impact,confidence,bv,tc,rr,js
"""
import sys
import json
import csv

FIELDS = [
    "id", "title", "description", "depends_on", "actor", "goal",
    "activity", "step", "pattern", "effort", "reach", "impact",
    "confidence", "bv", "tc", "rr", "js"
]


def main():
    if len(sys.argv) < 2:
        print("Usage: export_backlog_csv.py <story_map.json> --out <backlog.csv>", file=sys.stderr)
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
        print(f"[export-backlog] ERROR: Kann JSON nicht lesen: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Indizes erstellen
    activities = {a["id"]: a for a in data.get("activities", [])}
    
    step_title = {}
    for a in data.get("activities", []):
        for s in a.get("steps", []):
            step_title[s["id"]] = s["title"]
    
    # Rows erstellen
    rows = []
    for st in data.get("stories", []):
        row = {k: "" for k in FIELDS}
        
        row["id"] = st.get("id", "")
        row["title"] = st.get("title", "")
        row["description"] = st.get("description", "")
        row["depends_on"] = st.get("depends_on", "")
        row["actor"] = data.get("actor", "")
        row["goal"] = data.get("goal", "")
        row["activity"] = activities.get(st.get("activity_id"), {}).get("title", "")
        row["step"] = step_title.get(st.get("step_id"), "")
        row["pattern"] = st.get("pattern", "Workflow")
        
        # Ökonomische Felder optional vorbelegen (0/leer)
        for k in ["effort", "reach", "impact", "confidence", "bv", "tc", "rr", "js"]:
            row[k] = st.get(k, 0)
        
        rows.append(row)
    
    # CSV schreiben
    if not out:
        print("[export-backlog] Hinweis: --out <backlog.csv> nicht angegeben, schreibe nach stdout")
        writer = csv.DictWriter(sys.stdout, fieldnames=FIELDS)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    else:
        try:
            with open(out, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDS)
                writer.writeheader()
                for r in rows:
                    writer.writerow(r)
            print(f"[export-backlog] ✓ Geschrieben: {out} ({len(rows)} Stories)")
        except Exception as e:
            print(f"[export-backlog] ERROR: Kann CSV nicht schreiben: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
