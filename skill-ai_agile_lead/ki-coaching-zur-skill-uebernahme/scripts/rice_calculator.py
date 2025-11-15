#!/usr/bin/env python3
# RICE Calculator - Reach, Impact, Confidence, Effort
import csv
import sys


def die(msg, code=1):
    print(f"[RICE] {msg}", file=sys.stderr)
    sys.exit(code)


def main():
    if len(sys.argv) < 2:
        die("Bitte CSV-Datei angeben. Siehe Header in Datei assets/examples/example-prioritization-sheet.csv")
    
    infile = sys.argv[1]
    outfile = None
    
    if "--out" in sys.argv:
        idx = sys.argv.index("--out")
        if idx + 1 < len(sys.argv):
            outfile = sys.argv[idx + 1]
    
    if outfile is None:
        outfile = infile

    rows = []
    with open(infile, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                reach = float(row["reach"])
                impact = float(row["impact"])
                confidence = float(row["confidence"])
                effort = float(row["effort"])
                
                if effort <= 0:
                    die(f"Effort muss > 0 sein (id={row.get('id')})")
                
                rice = (reach * impact * confidence) / effort
                row["rice"] = f"{rice:.4f}"
                rows.append(row)
            except KeyError as e:
                die(f"Fehlende Spalte: {e}")
            except ValueError:
                die(f"Nicht-numerischer Wert entdeckt (id={row.get('id')}).")
    
    rows.sort(key=lambda x: float(x["rice"]), reverse=True)
    
    with open(outfile, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    
    print(f"[RICE] geschrieben: {outfile} (Datensätze: {len(rows)})")


if __name__ == "__main__":
    main()
