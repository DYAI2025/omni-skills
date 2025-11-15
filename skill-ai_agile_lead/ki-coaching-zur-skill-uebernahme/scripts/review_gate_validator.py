#!/usr/bin/env python3
# Review Gate Validator - validates gate record JSON
import sys
import json
import datetime

REQUIRED = ["gate_name", "date", "reviewers", "decision", "rationale", "risks", "next_actions"]
GATES = {"Ideation", "Backlog", "Execution", "Final"}
DECISIONS = {"approve", "changes", "reject"}


def die(msg, code=1):
    print(f"[Gate] {msg}", file=sys.stderr)
    sys.exit(code)


def main():
    if len(sys.argv) < 2:
        die("Bitte JSON-Datei angeben.")
    
    path = sys.argv[1]
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        die(f"Kann JSON nicht lesen: {e}")

    for k in REQUIRED:
        if k not in data:
            die(f"Pflichtfeld fehlt: {k}")
    
    if data["gate_name"] not in GATES:
        die(f"gate_name ungültig: {data['gate_name']}")
    
    try:
        datetime.date.fromisoformat(data["date"])
    except ValueError:
        die("date muss ISO-Format YYYY-MM-DD haben.")
    
    if not isinstance(data["reviewers"], list) or not data["reviewers"]:
        die("reviewers muss nicht-leere Liste sein.")
    
    if data["decision"] not in DECISIONS:
        die(f"decision ungültig: {data['decision']}")
    
    for fld in ["rationale", "risks", "next_actions"]:
        if not str(data[fld]).strip():
            die(f"{fld} darf nicht leer sein.")
    
    print("[Gate] valid")
    sys.exit(0)


if __name__ == "__main__":
    main()
