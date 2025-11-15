#!/usr/bin/env python3
# WSJF Calculator - Weighted Shortest Job First
import csv
import sys


def die(msg, code=1):
    print(f"[WSJF] {msg}", file=sys.stderr)
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
                bv = float(row["bv"])
                tc = float(row["tc"])
                rr = float(row["rr"])
                js = float(row["js"])
                
                if js <= 0:
                    die(f"Job Size (js) muss > 0 sein (id={row.get('id')})")
                
                cod = bv + tc + rr
                wsjf = cod / js
                row["cod"] = f"{cod:.4f}"
                row["wsjf"] = f"{wsjf:.4f}"
                rows.append(row)
            except KeyError as e:
                die(f"Fehlende Spalte: {e}")
            except ValueError:
                die(f"Nicht-numerischer Wert entdeckt (id={row.get('id')}).")
    
    rows.sort(key=lambda x: float(x["wsjf"]), reverse=True)
    
    with open(outfile, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    
    print(f"[WSJF] geschrieben: {outfile} (Datensätze: {len(rows)})")


if __name__ == "__main__":
    main()
